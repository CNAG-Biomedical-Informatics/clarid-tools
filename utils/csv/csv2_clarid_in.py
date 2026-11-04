#!/usr/bin/env python3
"""
csv2_clarid_in.py

Unified TSV -> CSV transformer for either 'biosample' or 'subject' data,
using per-field pipelines defined in YAML, with flexible subject_id handling.

$VERSION taken from ClarID::Tools

Copyright (C) 2025 Manuel Rueda - CNAG

License: Artistic License 2.0

If this program helps you in your research, please cite.
"""
import argparse
import csv
import gzip
import sys
from pathlib import Path

import yaml
from typing import Optional, List, Dict, Any

# Resolve the shared package relative to this script, not the working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from clarid_preprocessing.transforms import apply_ops

# --- I/O Helpers ------------------------------------------------------------

def open_input(path: str):
    return gzip.open(path, 'rt') if path.endswith('.gz') else open(path, 'r', newline='')

def open_output(path: str):
    return gzip.open(path, 'wt', newline='') if path.endswith('.gz') else open(path, 'w', newline='')

# --- Row blankness helpers --------------------------------------------------

def _is_blank_str(v: Optional[str]) -> bool:
    return v is None or (isinstance(v, str) and v.strip() == '')

def _is_empty_row(row: Dict[Any, Any]) -> bool:
    """
    Consider a row empty if:
      - all named fields are blank, and
      - any overflow fields under key None (from extra delimiters) are also blank.
    """
    named_blank = all(_is_blank_str(v) for k, v in row.items() if k is not None)
    extras = row.get(None)
    extras_blank = True
    if extras is not None:
        # csv.DictReader stores overflow as a list
        extras_blank = all(_is_blank_str(x) for x in extras)
    return named_blank and extras_blank

# --- Main -------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Unified parser for biosample or subject')
    parser.add_argument('--entity', choices=['biosample', 'subject'], required=True,
                        help='Which mapping entity to use')
    parser.add_argument('-i', '--input',   required=True, help='Input file (gz ok)')
    parser.add_argument('-o', '--output',  required=True, help='Output CSV file (gz ok)')
    parser.add_argument('-m', '--mapping', required=True, help='YAML mapping file')
    parser.add_argument('-d', '--delimiter', default='\t',
                        help="Input delimiter (default: tab). Use ',' for CSV.")
    args = parser.parse_args()

    cfg: Dict[str, Any] = yaml.safe_load(Path(args.mapping).read_text())
    fields_cfg    = cfg['fields']
    out_headers   = cfg['output_headers']
    static_fields = cfg.get('static_fields', {})

    # If subject_id has a source, we will be in "group" mode
    subj_cfg = fields_cfg.get('subject_id', {})
    subj_src = subj_cfg.get('source')
    subj_ops = subj_cfg.get('operations', [])

    with open_input(args.input) as infile:
        reader = csv.DictReader(infile, delimiter=args.delimiter)

        # Validate declared source columns
        missing = [fc['source'] for fc in fields_cfg.values()
                   if fc.get('source') and fc['source'] not in reader.fieldnames]
        if missing:
            sys.exit(f"ERROR: Missing columns: {missing}")

        with open_output(args.output) as outfile:
            writer = csv.writer(outfile, lineterminator='\n')
            writer.writerow(out_headers)

            counter = 0
            subject_counter = 0
            last_raw_subject = None

            for row in reader:
                # Skip completely empty or overflow-only rows
                if _is_empty_row(row):
                    continue

                # In group-mode, skip any row where the raw subject key is missing/blank
                if subj_src and _is_blank_str(row.get(subj_src)):
                    continue

                counter += 1
                out: List[str] = []
                for col in out_headers:
                    fc = fields_cfg.get(col, {})

                    if col == 'subject_id':
                        if subj_src:
                            raw = row.get(subj_src)
                            raw = apply_ops(raw, subj_ops)  # type: ignore
                            if raw != last_raw_subject:
                                subject_counter += 1
                                last_raw_subject = raw
                            val = str(subject_counter)
                        else:
                            subject_counter += 1
                            val = str(subject_counter)
                    else:
                        val = row.get(fc.get('source')) if fc.get('source') else None
                        val = apply_ops(val, fc.get('operations'))  # type: ignore
                        if (val is None or val == '') and col in static_fields:
                            val = static_fields[col]

                    out.append(val or '')
                writer.writerow(out)

    print(f"Wrote {args.output} ({counter} records)")

if __name__ == '__main__':
    main()
