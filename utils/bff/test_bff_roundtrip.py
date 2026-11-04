"""Real CLI round trips; requires the normal ClarID Perl dependencies."""
import csv
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from bff2_clarid_in import FIELDS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def read_csv(path):
    with path.open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))


class RoundTripTests(unittest.TestCase):
    def check_entity(self, entity, filename):
        expected = read_csv(HERE / f'fixtures/expected_{entity}.csv')
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            source = folder / 'input.csv'
            result = subprocess.run([
                sys.executable, str(HERE / 'bff2_clarid_in.py'), '--entity', entity,
                '-i', str(HERE / f'fixtures/{filename}.json'),
                '-m', str(HERE / f'{entity}_mapping.yaml'), '-o', str(source),
                '--subject-map', str(HERE / 'fixtures/subject_numbers.csv'),
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            mapped = read_csv(source)
            for fmt, column in [('human', 'clar_id'), ('stub', 'stub_id')]:
                with self.subTest(entity=entity, format=fmt):
                    encoded = folder / f'{fmt}.csv'
                    base = ['perl', str(ROOT / 'bin/clarid-tools'), 'code', '--entity', entity,
                            '--format', fmt, '--sep', ',', '--codebook',
                            str(ROOT / 'share/versions/0.04/clarid-codebook.yaml')]
                    result = subprocess.run(base + ['--action', 'encode', '--infile', str(source),
                        '--outfile', str(encoded)], capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    rows = read_csv(encoded)
                    self.assertEqual([{key: row[key] for key in ('unique_id', 'subject_id', column)}
                                      for row in rows],
                                     [{key: row[key] for key in ('unique_id', 'subject_id', column)}
                                      for row in expected])
                    if entity == 'biosample':
                        self.assertEqual(rows[0][column], rows[1][column])
                        self.assertNotEqual(rows[0]['unique_id'], rows[1]['unique_id'])
                        self.assertEqual([r['individual_id'] for r in rows],
                                         [r['individual_id'] for r in mapped])
                    # Only IDs enter the decoder: source columns cannot hide failures.
                    ids = folder / 'ids.csv'
                    with ids.open('w', newline='') as handle:
                        writer = csv.DictWriter(handle, fieldnames=['unique_id', column],
                                                extrasaction='ignore')
                        writer.writeheader(); writer.writerows(rows)
                    decoded = folder / 'decoded.csv'
                    result = subprocess.run(base + ['--action', 'decode', '--infile', str(ids),
                        '--outfile', str(decoded), '--with-condition-name'], capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    recovered = read_csv(decoded)
                    self.assertEqual(len(recovered), len(mapped))
                    for before, after in zip(mapped, recovered):
                        self.assertEqual(before['unique_id'], after['unique_id'])
                        self.assertEqual(before['subject_id'], after['subject_id'])
                        self.assertTrue(after['condition_name'])
                        for field in FIELDS[entity]:
                            value = before[field]
                            if field == 'study':
                                value = 'CT' if fmt == 'stub' else 'CNAG_Test'
                            if entity == 'subject' and fmt == 'human' and field == 'sex' and value == 'Not Available':
                                value = 'NAV'
                            self.assertEqual(value, after[field], f'{entity}/{fmt}/{field}')

    def test_subject_roundtrip(self):
        self.check_entity('subject', 'individuals')

    def test_biosample_roundtrip(self):
        self.check_entity('biosample', 'biosamples')


if __name__ == '__main__':
    unittest.main()
