# Fictional test records

Three individuals and five biosamples, written by hand for converter tests.
They are not CINECA records or extracts from any patient dataset. Clinical and
experimental combinations are test inputs, not biological observations.

- EX-S1 and EX-S2 deliberately share a ClarID, but keep separate source IDs.
- EX-S3 contains a JSON string under `info.clarid` and only a batch number.
- EX-S4 has only a replicate number; EX-S5 lacks most optional metadata.
- EX-S5 maps missing species to Unknown (stub `00`).
- `subject_numbers.csv` represents an existing numeric mapping, starting at 41.
- `expected_*.csv` records the expected labels with codebook 0.04.

The extra `info` fields are example mapping inputs, not new Beacon requirements.
Z00.0 is an explicitly supplied test convention, never a missing-value default.
Full datasets are used only for local integration checks and are not copied here.
