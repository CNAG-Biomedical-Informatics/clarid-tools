**Clarid-Tools** has 3 subcommands:

`code`, `qrcode` and `validate`.

---

## 📦 `clarid-tools code` Options

```bash
clarid-tools [-h] [long options ...]
```

- `--action`: *String*  
  `encode | decode`

- `--age_group`: *String*  
  Age group

- `--assay`: *String*  
  Assay key

- `--batch`: *String*  
  Batch

- `--clar_id`: *String*  
  ID to decode (use `--clar_id` or `--stub_id`)

- `--codebook`: *String*  
  Path to `codebook.yaml`

- `--condition`: *String*  
  Condition key or ICD-10 code

- `--duration`: *String*  
  Duration: `P[0-9][D|W|M|Y]` or `P0N` (Not Available)

- `--entity`: *String*  
  `biosample | subject`  
  (accepts synonyms: `biospecimen -> biosample`; `individual -> subject`)

- `--format`: *String*  
  `human | stub`

- `--icd10_map`: *String*  
  Path to ICD-10 map JSON

- `--icd10_order`: *String*  
  Path to `icd10_order.json`

- `--infile`: *String*  
  Bulk input CSV/TSV

- `--max_conditions`: Int
   Maximum number of ICD-10 codes allowed

- `--outfile`: *String*  
  Bulk output file

- `--project`: *String*  
  Project key

- `--replicate`: *Int*  
  Replicate number

- `--sample_type`: *String*  
  Sample type key

- `--sep`: *String*  
  Separator

- `--sex`: *String*  
  Sex

- `--species`: *String*  
  Species key

- `--study`: *String*  
  Study

- `--subject_id`: *Int*  
  Subject ID

- `--subject_id_base62_width`: *Int*  
  Number of Base-62 characters to use for subject ID stubs

- `--subject_id_pad_length`: *Int*  
  Decimal padding width for subject IDs in biosample/subject human format

- `--timepoint`: *String*  
  Timepoint

- `--tissue`: *String*  
  Tissue key

- `--type`: *String*  
  Type

- `--with_condition_name`:  
  Append human-readable `condition_name` on decode

- `--usage`, `-h`, `--help`, `--man`:  
  Show help messages or manual


## 🔍 `clarid-tools validate` Options

```bash
clarid-tools validate [-h] [long options ...]
```

- `--codebook`: *String*  
  Path to your `codebook.yaml`

- `--debug`:  
  Self-validate the schema before use

- `--schema`: *String*  
  Path to JSON Schema file

- `--usage`, `-h`, `--help`, `--man`:  
  Show help messages or manual


## 🔳 `clarid-tools qrcode` Options

```bash
clarid-tools qrcode [-h] [long options ...]
```

- `--action`: *String*  
  `encode | decode`

- `--column`: *String*  
  Column name to read (defaults to `clar_id` or `stub_id`, encode only)

- `--input`: *String*  
  CSV file (encode) or directory of PNGs, or single PNG file (decode)

- `--outdir`: *String*  
  Where to write PNGs (encode only)

- `--outfile`: *String*  
  Where to write CSV (decode directory mode only)

- `--sep`: *String*  
  CSV separator

- `--size`: *Int*  
  Module size for `qrencode` (`-s` flag)

- `--usage`, `-h`, `--help`, `--man`:  
  Show help messages or manual
