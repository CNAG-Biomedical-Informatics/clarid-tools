#!/usr/bin/env python3
"""Prepare ClarID input CSV from Beacon v2/BFF individuals or biosamples JSON.

Copyright (C) 2026 Manuel Rueda - CNAG
License: Artistic License 2.0
"""
import argparse
import csv
from datetime import date
import gzip
import json
from pathlib import Path
import sys

import yaml

# Resolve the shared package relative to this script, not the working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from clarid_preprocessing.transforms import apply_ops

FIELDS = {
    'biosample': ['project', 'species', 'tissue', 'sample_type', 'assay',
                 'condition', 'timepoint', 'duration', 'batch', 'replicate'],
    'subject': ['study', 'type', 'condition', 'sex', 'age_group'],
}


def headers(entity):
    return ['unique_id', *(['individual_id'] if entity == 'biosample' else []),
            'subject_id', *FIELDS[entity]]


def open_text(path, mode='rt'):
    opener = gzip.open if str(path).endswith('.gz') else open
    return opener(path, mode, encoding='utf-8-sig' if mode == 'rt' else 'utf-8', newline='')


def source_value(record, path):
    """Resolve dotted paths, including explicitly indexed arrays and JSON strings."""
    value = record
    for part in path.split('.'):
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except ValueError:
                raise ValueError('Cannot traverse the configured JSON path') from None
        if isinstance(value, dict):
            value = value.get(part)
        elif isinstance(value, list) and part.isdecimal():
            value = value[int(part)] if int(part) < len(value) else None
        elif value is None:
            return None
        else:
            raise ValueError('JSON path needs an object key or an explicit list index')
    if isinstance(value, (dict, list)):
        raise ValueError('Mapped field must select a scalar, not an object or list')
    return None if value is None else str(value)


def prior_subjects(path):
    if path is None:
        return {}
    with open_text(path) as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames or []
        key = 'individual_id' if 'individual_id' in columns else 'unique_id'
        if key not in columns or 'subject_id' not in columns:
            raise ValueError('Subject map needs individual_id (or subject unique_id) and subject_id')
        mapping, owners = {}, {}
        for row in reader:
            identifier, number = row.get(key), row.get('subject_id') or ''
            if not identifier or identifier != identifier.strip() or not number.isdecimal():
                raise ValueError('Invalid subject map')
            number = int(number)
            if identifier in mapping and mapping[identifier] != number:
                raise ValueError('Conflicting subject-number assignments')
            if number in owners and owners[number] != identifier:
                raise ValueError('Different subjects share a numeric subject_id')
            mapping[identifier], owners[number] = number, identifier
        return mapping


def mapped_value(record, spec):
    value = source_value(record, spec['source']) if spec.get('source') else None
    for operation in spec.get('operations', []):
        if isinstance(operation, dict) and 'age_at' in operation:
            if set(operation) != {'age_at'} or not isinstance(operation['age_at'], str):
                raise ValueError('age_at requires an observation-date path')
            observed = source_value(record, operation['age_at'])
            if not value or not observed:
                value = None
            else:
                # Use the recorded calendar dates, never today's date.
                dob, when = date.fromisoformat(value[:10]), date.fromisoformat(observed[:10])
                value = str(when.year - dob.year - ((when.month, when.day) < (dob.month, dob.day)))
        else:
            value = apply_ops(value, [operation])
    return value


def subject_records(records, individual_id_path, first_by):
    """Choose an explicitly requested baseline, or check all mapped snapshots."""
    grouped = {}
    for index, record in enumerate(records, 1):
        try:
            identifier = source_value(record, individual_id_path)
            value = source_value(record, first_by) if first_by else None
            rank = date.fromisoformat(value[:10]) if value else date.max
        except (ValueError, TypeError):
            raise ValueError(f'Record {index}: invalid individual ID path or observation date') from None
        if not identifier or identifier != identifier.strip():
            raise ValueError(f'Record {index}: missing or invalid individual ID')
        grouped.setdefault(identifier, []).append((rank, index, record))
    selected = []
    for identifier, items in sorted(grouped.items()):
        earliest = min(item[0] for item in items)
        selected.extend((index, identifier, record) for rank, index, record in items
                        if not first_by or rank == earliest)
    return selected


def prepare(records, config, previous=None, entity='biosample', individual_id_path='id', first_by=None):
    if entity not in FIELDS:
        raise ValueError('Entity must be subject or biosample')
    if entity != 'subject' and (first_by or individual_id_path != 'id'):
        raise ValueError('Individual ID and baseline options apply only to subjects')
    if not isinstance(records, list) or not records:
        raise ValueError('Input must be a non-empty JSON array of records')
    if not isinstance(config, dict) or set(config) - {'fields', 'static_fields'}:
        raise ValueError('Mapping supports fields and static_fields')
    fields, defaults = config.get('fields', {}), config.get('static_fields', {})
    if not isinstance(fields, dict) or not isinstance(defaults, dict):
        raise ValueError('Invalid mapping')
    if (set(fields) | set(defaults)) - set(FIELDS[entity]):
        raise ValueError('Unsupported ClarID field; source identities are preserved automatically')
    for field, spec in fields.items():
        if (not isinstance(spec, dict) or set(spec) - {'source', 'operations'}
                or ('source' in spec and (not isinstance(spec['source'], str) or not spec['source']))
                or not isinstance(spec.get('operations', []), list)
                or any(isinstance(op, dict) and len(op) != 1 for op in spec.get('operations', []))):
            raise ValueError(f'Invalid mapping for {field}')
    seen = set()
    required = ('id', 'individualId') if entity == 'biosample' else ('id',)
    for index, record in enumerate(records, 1):
        if not isinstance(record, dict) or any(
                not isinstance(record.get(key), str) or not record[key].strip()
                or record[key] != record[key].strip() for key in required):
            raise ValueError(f'Record {index}: {", ".join(required)} must be non-empty strings')
        if entity == 'biosample' and record['id'] in seen:
            raise ValueError(f'Record {index}: duplicate source biosample id')
        seen.add(record['id'])
    selected = (subject_records(records, individual_id_path, first_by) if entity == 'subject' else
                [(index, record['individualId'], record) for index, record in enumerate(records, 1)])
    subjects = {identifier for _, identifier, _ in selected}
    numbers = dict(previous or {})
    if (any(type(number) is not int or number < 0 for number in numbers.values())
            or len(set(numbers.values())) != len(numbers)):
        raise ValueError('Invalid previous subject-number mapping')
    next_number = max(numbers.values(), default=0) + 1
    for identifier in sorted(subjects - numbers.keys()):
        numbers[identifier] = next_number
        next_number += 1
    output = {}
    for index, identifier, record in selected:
        row = dict(unique_id=identifier if entity == 'subject' else record['id'],
                   subject_id=numbers[identifier])
        if entity == 'biosample':
            row['individual_id'] = identifier
        for field in FIELDS[entity]:
            spec = fields.get(field, {})
            try:
                value = mapped_value(record, spec)
                if value is None or (isinstance(value, str) and not value.strip()):
                    value = defaults.get(field)
                if isinstance(value, (dict, list)):
                    raise ValueError('Expected scalar')
                row[field] = '' if value is None else str(value).strip()
            except (ValueError, TypeError, KeyError, AttributeError, IndexError):
                raise ValueError(f'Record {index}: invalid mapping for {field}') from None
            if not row[field] and field not in ('batch', 'replicate'):
                raise ValueError(f'Record {index}: missing {field}; supply an explicit mapping or fallback')
        if row['unique_id'] in output and output[row['unique_id']] != row:
            raise ValueError(f'Record {index}: conflicting subject metadata; select a baseline explicitly')
        output[row['unique_id']] = row
    return list(output.values())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--entity', choices=['biosample', 'subject'], required=True)
    parser.add_argument('-i', '--input', type=Path, required=True, help='BFF JSON array, optionally .gz')
    parser.add_argument('-m', '--mapping', type=Path, required=True, help='YAML field mapping')
    parser.add_argument('-o', '--output', type=Path, required=True, help='New ClarID input CSV, optionally .gz')
    parser.add_argument('--subject-map', type=Path, help='Existing subject ClarID CSV or previous output; preserve subject numbers')
    parser.add_argument('--individual-id-path', default='id', help='Subject identity path; e.g. patient_id for clinical snapshots')
    parser.add_argument('--first-by', help='Subjects only: choose earliest recorded date at this path (missing dates last)')
    args = parser.parse_args()
    try:
        with open_text(args.input) as handle:
            records = json.load(handle)
        with open_text(args.mapping) as handle:
            config = yaml.safe_load(handle)
        rows = prepare(records, config, prior_subjects(args.subject_map), args.entity,
                       args.individual_id_path, args.first_by)
        with open_text(args.output, 'xt') as handle:
            writer = csv.DictWriter(handle, fieldnames=headers(args.entity), lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)
    except (ValueError, TypeError, OSError, EOFError, csv.Error, yaml.YAMLError) as error:
        message = str(error) if type(error) is ValueError else 'Check input files, mapping syntax and the new output path'
        parser.exit(2, f'Error: {message}\n')
    print(f'Prepared {len(rows)} {args.entity} records.')
    if args.subject_map is None:
        print('Assigned subject numbers in sorted ID order. Reuse this CSV with --subject-map for subsequent preparations.')


if __name__ == '__main__':
    main()
