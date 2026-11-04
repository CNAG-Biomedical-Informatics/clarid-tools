"""Shared mapping transformations for ClarID preprocessing utilities.

Copyright (C) 2025 Manuel Rueda - CNAG
License: Artistic License 2.0
"""
import re
from typing import Optional, List, Dict, Callable, Any, Set

# --- Primitive operations ---------------------------------------------------

def strip_quotes(v: Optional[str]) -> Optional[str]:
    """Trim whitespace then remove surrounding single/double quotes."""
    if v is None:
        return None
    vs = v.strip()
    return vs.strip("'\"")

def trim(v: Optional[str]) -> Optional[str]:
    """Trim leading/trailing whitespace."""
    if v is None:
        return None
    return v.strip()

def collapse_spaces(v: Optional[str]) -> Optional[str]:
    """Collapse all runs of whitespace into a single space."""
    if v is None:
        return None
    return ' '.join(v.split())

def remove_all_spaces(v: Optional[str]) -> Optional[str]:
    """Remove all whitespace characters."""
    if v is None:
        return None
    return ''.join(v.split())

def remove_suffix(v: Optional[str], suffix: str) -> Optional[str]:
    """Case-insensitive remove suffix, plus trailing whitespace."""
    if v is None:
        return None
    if v.lower().endswith(suffix.lower()):
        return v[:-len(suffix)].rstrip()
    return v

def map_values(v: Optional[str], mapping: Dict[Any, Any]) -> Optional[str]:
    """Map raw value to new via dict, defaulting to original."""
    return mapping.get(v, v)

def normalize_sex(v: Optional[str]) -> Optional[str]:
    """
    Capitalize gender, or return None if blank (so static_fields can apply).
    If the literal string 'unknown' is provided, it will become 'Unknown'.
    """
    if v is None or not v.strip():
        return None
    return v.strip().capitalize()

def bucketize_age(v: Optional[str], groups: List[Dict[str, Any]]) -> Optional[str]:
    """
    Convert numeric age string into named bucket,
    return None if the cell is truly blank (so static_fields can apply),
    otherwise if parsing/bucketing fails, return 'Unknown'.
    """
    if v is None or not v.strip():
        return None
    try:
        age = int(v)  # type: ignore
    except Exception:
        return 'Unknown'
    for g in groups:
        if g['min'] <= age <= g['max']:
            return g['name']
    return 'Unknown'

def normalize_multivalue(v: Optional[str], cfg: Dict[str, Any]) -> Optional[str]:
    """
    Split a multi-value string on configured delimiters, trim tokens,
    map each via optional 'map_values', drop empties, optional dedupe,
    then join with 'join_with' (default ';').
    """
    if v is None or not v.strip():
        return None

    delims = cfg.get('delimiters', [',', ';', '|', '/'])
    join_with = cfg.get('join_with', ';')
    mapping = cfg.get('map_values', {}) or cfg.get('mapping', {})
    drop_empty = cfg.get('drop_empty', True)
    dedupe = cfg.get('dedupe', False)

    pat = '|'.join(re.escape(d) for d in delims)
    tokens = re.split(pat, v)

    out: List[str] = []
    seen: Set[str] = set()
    for t in tokens:
        t = t.strip().strip("'\"")
        if drop_empty and not t:
            continue
        mapped = mapping.get(t, t)
        if dedupe:
            if mapped in seen:
                continue
            seen.add(mapped)
        out.append(mapped)

    return join_with.join(out)

def days_to_iso8601_bin(v: Optional[str], cfg: Dict[str, Any]) -> Optional[str]:
    """
    Convert a numeric day count into a 3-char ISO8601-like bin: 'P{n}{U}'
    where n in 0..9 and U in {D, W, M, Y}. Strategy:
      - blank -> None (so static_fields can apply)
      - parse error / negative -> cfg['on_error'] (default None)
      - prefer 'D' if <= 9; else try 'W' (days/7), then 'M' (~30), then 'Y' (~365)
      - rounding: floor|round|ceil (default: floor)
      - if years > 9, clamp to P9Y
    """
    if v is None or not str(v).strip():
        return None

    s = str(v).strip()
    try:
        days = float(s)
    except Exception:
        return cfg.get('on_error')  # default None

    if days < 0:
        return cfg.get('on_error')

    rounding = str(cfg.get('rounding', 'floor')).lower()
    def R(x: float) -> int:
        import math
        if rounding == 'ceil':
            return int(math.ceil(x))
        if rounding == 'round':
            return int(round(x))
        return int(math.floor(x))

    units: List[str] = cfg.get('units', ['D', 'W', 'M', 'Y'])

    # Try days
    if 'D' in units and days <= 9:
        return f'P{int(days)}D'

    # Try weeks
    if 'W' in units:
        w = R(days / 7.0)
        if 1 <= w <= 9:
            return f'P{w}W'

    # Try months (~30)
    if 'M' in units:
        m = R(days / 30.0)
        if 1 <= m <= 9:
            return f'P{m}M'

    # Fallback to years (~365), clamp to 1..9
    if 'Y' in units:
        y = R(days / 365.0)
        if y < 1:
            y = 1
        if y > 9:
            y = 9
        return f'P{y}Y'

    return cfg.get('on_error')

# Registry of zero-arg primitives
PRIMITIVES: Dict[str, Callable[[Optional[str]], Optional[str]]] = {
    'strip_quotes': strip_quotes,
    'trim': trim,
    'collapse_spaces': collapse_spaces,
    'remove_all_spaces': remove_all_spaces,
    'normalize_sex': normalize_sex,
}

# --- Dispatcher -------------------------------------------------------------

def apply_ops(value: Optional[str], ops: Optional[List[object]]) -> Optional[str]:
    """
    Apply each operation in the exact sequence provided:
      - string -> zero-arg primitive
      - dict with 'map_values' -> map_values
      - dict with other keys -> special ops inline
    """
    v = value
    if not ops:
        return v

    for op in ops:
        if isinstance(op, str):
            fn = PRIMITIVES.get(op)
            if not fn:
                raise ValueError(f"Unknown op '{op}'")
            v = fn(v)

        elif isinstance(op, dict):
            name, arg = next(iter(op.items()))
            if name == 'map_values':
                v = map_values(v, arg)            # run mapping right here
            elif name == 'remove_suffix':
                v = remove_suffix(v, arg)         # inline remove_suffix
            elif name == 'bucketize_age':
                v = bucketize_age(v, arg)         # inline bucketize_age
            elif name == 'normalize_multivalue':
                v = normalize_multivalue(v, arg)  # inline multivalue normalize
            elif name == 'days_to_iso8601_bin':
                v = days_to_iso8601_bin(v, arg)
            else:
                raise ValueError(f"Unknown op '{name}'")

        else:
            raise ValueError(f"Invalid op entry: {op}")

    return v
