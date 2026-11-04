import csv
import gzip
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import yaml

from bff2_clarid_in import prepare, prior_subjects, source_value


def config():
    return {'fields': {'tissue': {'source': 'sampleOriginType.id', 'operations': [
        {'map_values': {'UBERON:0000178': 'Blood'}}]}},
        'static_fields': {'project': 'CNAG-Test', 'species': 'Human',
            'sample_type': 'Not Available', 'assay': 'Not Available',
            'condition': 'C22.0', 'timepoint': 'Not Available', 'duration': 'P0N'}}


def sample(identifier='S1', subject='P1'):
    return {'id': identifier, 'individualId': subject,
            'sampleOriginType': {'id': 'UBERON:0000178'}}


class BffInputTests(unittest.TestCase):
    def test_subject_fixture_and_biosample_linkage(self):
        root = Path(__file__).parent
        records = json.loads((root / 'fixtures/individuals.json').read_text())
        cfg = yaml.safe_load((root / 'subject_mapping.yaml').read_text())
        numbers = prior_subjects(root / 'fixtures/subject_numbers.csv')
        rows = prepare(records, cfg, numbers, entity='subject')
        self.assertEqual([r['subject_id'] for r in rows], [41, 42, 43])
        self.assertEqual([r['age_group'] for r in rows], ['Age40to49', 'Age30to39', 'Not Available'])
        self.assertEqual(rows[-1]['sex'], 'Not Available')
        records = json.loads((root / 'fixtures/biosamples.json').read_text())
        cfg = yaml.safe_load((root / 'biosample_mapping.yaml').read_text())
        biosamples = prepare(records, cfg, numbers)
        self.assertEqual([r['subject_id'] for r in biosamples], [41, 41, 42, 42, 43])
        self.assertEqual(biosamples[2]['assay'], 'RNA_seq')
        self.assertEqual(biosamples[2]['batch'], '2')
        self.assertEqual(biosamples[-1]['duration'], 'P0N')

    def test_snapshot_conflicts_and_explicit_baseline(self):
        cfg = {'static_fields': {'study': 'CNAG-Test', 'type': 'Case', 'condition': 'C22.0',
                                'age_group': 'Not Available'},
               'fields': {'sex': {'source': 'sex.label'}}}
        early = {'id': 'visit-1', 'patient_id': 'P1', 'sex': {'label': 'Male'},
                 'info': {'event_date': '2020-01-01'}}
        late = dict(early, id='visit-2', sex={'label': 'Female'}, info={'event_date': '2021-01-01'})
        with self.assertRaisesRegex(ValueError, 'conflicting'):
            prepare([early, late], cfg, entity='subject', individual_id_path='patient_id')
        rows = prepare([late, early], cfg, entity='subject', individual_id_path='patient_id',
                       first_by='info.event_date')
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['sex'], 'Male')
        self.assertEqual(rows[0]['unique_id'], 'P1')
        with self.assertRaisesRegex(ValueError, 'conflicting'):
            prepare([early, dict(late, info=early['info'])], cfg, entity='subject',
                    individual_id_path='patient_id', first_by='info.event_date')

    def test_age_at_observation_and_blank_fallback(self):
        cfg = {'static_fields': {'study': 'CNAG-Test', 'type': 'Case', 'condition': 'C22.0',
                                'sex': 'Not Available', 'age_group': 'Not Available'},
               'fields': {'age_group': {'source': 'info.dob', 'operations': [
                   {'age_at': 'info.observed'}, {'bucketize_age': [
                       {'min': 30, 'max': 39, 'name': 'Age30to39'}]}]},
                   'sex': {'source': 'sex.label'}}}
        record = {'id': 'P1', 'sex': {'label': '  '},
                  'info': {'dob': '1980-02-01', 'observed': '2020-01-01'}}
        row = prepare([record], cfg, entity='subject')[0]
        self.assertEqual(row['age_group'], 'Age30to39')
        self.assertEqual(row['sex'], 'Not Available')
        record['info'].pop('observed')
        self.assertEqual(prepare([record], cfg, entity='subject')[0]['age_group'], 'Not Available')

    def test_identity_and_repeated_characteristics(self):
        rows = prepare([sample('S2'), sample('S1')], config())
        self.assertEqual([r['unique_id'] for r in rows], ['S2', 'S1'])
        self.assertEqual([r['subject_id'] for r in rows], [1, 1])
        self.assertEqual(rows[0]['tissue'], 'Blood')
        self.assertEqual(rows[0]['batch'], '')
        self.assertEqual(rows[0]['replicate'], '')

    def test_order_independent_numbers_and_previous_mapping(self):
        records = [sample('S2', 'P2'), sample('S1', 'P1')]
        self.assertEqual([r['subject_id'] for r in prepare(records, config())], [2, 1])
        self.assertEqual([r['subject_id'] for r in prepare(records, config(), {'P1': 50})], [51, 50])

    def test_nested_json_and_explicit_index(self):
        record = {'info': {'details': '[{"name":"Blood"}]'}}
        self.assertEqual(source_value(record, 'info.details.0.name'), 'Blood')
        with self.assertRaises(ValueError): source_value(record, 'info.details.name')
        with self.assertRaises(ValueError): source_value(record, 'info')

    def test_missing_condition_and_duplicate_id(self):
        cfg = config(); cfg['static_fields'].pop('condition')
        with self.assertRaisesRegex(ValueError, 'missing condition'): prepare([sample()], cfg)
        with self.assertRaisesRegex(ValueError, 'duplicate'): prepare([sample(), sample()], config())
        with self.assertRaises(ValueError): prepare([{'id': 'S1'}], config())

    def test_subject_map_and_conflicts(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'subjects.csv'
            path.write_text('unique_id,subject_id\nP1,7\nP2,9\n')
            self.assertEqual(prior_subjects(path), {'P1': 7, 'P2': 9})
            path.write_text('individual_id,subject_id\nP1,7\nP1,7\n')
            self.assertEqual(prior_subjects(path), {'P1': 7})
            path.write_text('unique_id,subject_id\nP1,7\nP2,7\n')
            with self.assertRaises(ValueError): prior_subjects(path)

    def test_cli_gzip_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            with gzip.open(root / 'biosamples.json.gz', 'wt') as h: json.dump([sample()], h)
            (root / 'mapping.json').write_text(json.dumps(config()))
            command = [sys.executable, str(Path(__file__).with_name('bff2_clarid_in.py')),
                '--entity', 'biosample',
                '-i', str(root / 'biosamples.json.gz'), '-m', str(root / 'mapping.json'),
                '-o', str(root / 'out.csv.gz')]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            with gzip.open(root / 'out.csv.gz', 'rt') as h:
                self.assertEqual(list(csv.DictReader(h))[0]['unique_id'], 'S1')
            original = (root / 'out.csv.gz').read_bytes()
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)
            self.assertEqual((root / 'out.csv.gz').read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
