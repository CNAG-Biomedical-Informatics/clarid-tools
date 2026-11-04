# BFF → ClarID

Extract supported fields from Beacon v2/BFF **individuals or biosamples** into
ClarID-ready CSV, then use the existing encoder. No DuckDB or COHORTome is needed.
The original JSON remains the full source record.

## Quick start

Run from the ClarID repository with its Perl dependencies installed. The small,
fictional fixture is ready to try; use new output filenames for each run.

```bash
python3 -m pip install -r utils/csv/requirements.txt
python3 utils/bff/bff2_clarid_in.py --entity subject \
  -i utils/bff/fixtures/individuals.json -m utils/bff/subject_mapping.yaml \
  -o subjects_in.csv --subject-map utils/bff/fixtures/subject_numbers.csv

python3 utils/bff/bff2_clarid_in.py --entity biosample \
  -i utils/bff/fixtures/biosamples.json -m utils/bff/biosample_mapping.yaml \
  -o biosamples_in.csv --subject-map subjects_in.csv

bin/clarid-tools code --entity subject --action encode --format human \
  --codebook share/versions/0.04/clarid-codebook.yaml \
  --infile subjects_in.csv --sep ',' --outfile subjects_human.csv
```

For biosample encoding, use `--entity biosample` and `biosamples_in.csv`.
Use `--format stub` for compact labels; decode with `--with-condition-name`
for condition descriptions. The current checkout includes fixes for blank
batch/replicate CSV cells and missing-species stub decoding.

## Mapping

Copy the relevant mapping YAML and review it for your study. Project/study names
must exist in the codebook; retain any study-specific codebook with the output.

- Individual `id` becomes `unique_id`. Biosamples preserve their `id` as
  `unique_id` and their parent `individualId` as `individual_id`.
- `fields` selects dotted paths, such as `sampleOriginType.id`, and reuses the
  transformations from [`utils/csv`](../csv/README.md). Nothing is encoded here.
- JSON-valued strings are parsed only when a configured path enters them.
  Nested arrays need an explicit index, for example `info.details.0.label`.
  No first-element choice or clinical inference happens automatically.
- `static_fields` supplies explicit fallbacks for missing values. Unrecognized
  ontology codes are not silently converted to Unknown; the encoder validates
  mapped vocabulary against its codebook.
- The examples intentionally have **no default condition**. Review this mapping
  for the study. A reference sample does not automatically mean normal tissue,
  and a collection date alone does not establish elapsed time from baseline.
- Batch and replicate can be omitted. Do not invent them to make labels unique.

Only selected fields enter CSV. Input/output may be gzip-compressed. Existing
converter output files are never overwritten (the separate encoder may overwrite
its output). Input must be a JSON array, not an arbitrary Beacon API response.
The array is read into memory. This is not a whole-genome variation converter.

## Clinical snapshots and age

For one record per visit, use `--entity subject --individual-id-path patient_id`.
Identical mapped subject rows collapse into one; conflicting values fail.
To select a baseline explicitly, add `--first-by info.event_date`. The earliest
recorded calendar date wins, missing dates sort last, and conflicting ties fail.
No visit is silently selected by input order.

For a birth date, an `age_at` operation can precede the existing `bucketize_age`:

```yaml
age_group:
  source: info.phenopacket.dateOfBirth
  operations:
    - age_at: info.event_date
    - bucketize_age:
        - {min: 40, max: 49, name: Age40to49}
        # Include the other age bands used by your study.
```

Dates use the recorded ISO calendar-date component, never today's date. Missing
dates use the configured fallback. The paths above are examples of source `info`
metadata, not required Beacon fields. No general ontology-to-ICD mapping is inferred.

## Subject numbers and identity

`--subject-map` accepts a subject CSV with `unique_id,subject_id`, or a previous
output with `individual_id,subject_id`. Existing numbers are preserved; new
subjects receive numbers above the previous maximum. Without a map, numbers
are assigned by sorted subject ID, independent of biosample row order.

Keep the complete subject map when preparing subsets or later versions.
Generating a fresh mapping for a different subset can assign different numbers;
a subset output is not a replacement for the complete mapping.

**Different specimens may share a ClarID.** It describes their encoded
characteristics, not their unique database identity. The source biosample ID
is preserved, and repeated subjects share the same numeric subject ID.

To reproduce existing ClarIDs, reuse their subject map, codebook, field mappings
and baseline convention. Matching source IDs alone is not enough.

## Tests

```bash
python3 -m unittest discover -s utils/bff -p 'test_*.py'
```

The utility uses Python and PyYAML, like `utils/csv`. It does not modify BFF,
call a language model, download data or require COHORTome.
