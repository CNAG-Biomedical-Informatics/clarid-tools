# ClarID Specification Tables

## Biosample

### Human format  
**Delimiter:** `-`

| #  | Component   | Source field                | Type         | Pattern / Format                                           | Built from                                 |
|---:|-------------|-----------------------------|--------------|------------------------------------------------------------|---------------------------------------------|
| 1  | Project     | `project.code`              | string       | free string                                                | codebook value (if present)                    |
| 2  | Species     | `species.code`              | string       | 6-letter binomial acronym (e.g. `HomSap`)                   | codebook value                              |
| 3  | Subject ID  | `subject_id`                | integer→str  | zero-pad to 5 digits (default)                              | `sprintf("%0${pad}d",$sid)`                |
| 4  | Tissue      | `tissue.code`               | string       | exactly 3 letters `[A-Z]{3}`                                | codebook value                              |
| 5  | Sample Type | `sample_type.code`          | string       | exactly 3 letters `[A-Z]{3}`                                | codebook value                              |
| 6  | Assay       | `assay.code`                | string       | exactly 3 letters `[A-Z]{3}`                                | codebook value                              |
| 7  | Condition   | `condition`                 | string       | ICD-10 diagnose code(s) `[A-Z]\d{2}(?:\.\d+)?` (≤10),       | used verbatim (or concatenated with `+`)    |
| 8  | Timepoint   | `timepoint`                 | string       | alphanumeric events e.g. `Baseline`                   | codebook value                  |
| 9  | Duration    | `duration`                  | string       | ISO 8601 3-char (`P1D`,`P7W`,`P3M`,`P1Y`) or `P0N` (Not Available)                  | `duration_pattern`                         |
| 10 | Batch (opt) | `batch`                     | integer→str  | `B%02d` (e.g. `B01`)                                        | `batch_pattern`                            |
| 11 | Replicate (opt) | `replicate`             | integer→str  | `R%02d` (e.g. `R05`)                                        | `replicate_pattern`                        |

> Note (`duration`): The 3-character limit (PnU) is intentional, designed to keep timepoint duration compact and consistent, rather than attempting to represent every possible duration in full detail [isee duration binning](./pre-processing-script.md#duration-binning-days-iso8601-pnu).

### Stub format  
**Delimiter:** _(none)_

| #  | Component      | Source field                | Type            | Pattern / Format                       | Built from                                |
|---:|----------------|-----------------------------|-----------------|-----------------------------------------|--------------------------------------------|
| 1  | Project stub   | `project.stub_code`         | string          | free string                            | codebook value                             |
| 2  | Species stub   | `species.stub_code`         | string          |  2-char codebook stub (Base62 alphabet) | codebook value                             |
| 3  | Subject stub   | `subject_id`                | integer→Base62 | width 3 (default) — max 238,327        | 3-char Base62 from integer             |
| 4  | Tissue stub    | `tissue.stub_code`          | string          | 1–3 chars                              | codebook value                             |
| 5  | Sample Type stub | `sample_type.stub_code`   | string          | 1–3 chars                              | codebook value                             |
| 6  | Assay stub     | `assay.stub_code`           | string          | 1–3 chars                              | codebook value                             |
| 7  | Condition stub | `condition`                 | code→Base62    | N × 3-char Base62 stubs + 2-digit count (`%02d`)           | codebook order + 3-char Base62 from integer |
| 8  | Timepoint stub | `timepoint.stub_code`       | string          | 1–2 chars                              | codebook value                   |
| 9  | Duration stub  | `duration`                  | string          | digits+unit (e.g. `7W`)                 | `duration_pattern`                         |
| 10 | Batch stub (opt) | `batch`                  | integer         |  `B%02d` (e.g. `B01`)                     | `batch_pattern`                            |
| 11 | Replicate stub (opt) | `replicate`         | integer         | `R%02d` (e.g. `R05`)                       | `replicate_pattern`                        |

---

## Subject

### Human format  
**Delimiter:** `-`

| # | Component   | Source field           | Type         | Pattern / Format                      | Built from                               |
|--:|-------------|------------------------|--------------|----------------------------------------|-------------------------------------------|
| 1 | Study       | `study`                | string       | free string                           | codebook value (if present)                  |
| 2 | Subject ID  | `subject_id`           | integer→str  | zero-pad to 5 digits (default)         | `sprintf("%0${pad}d",$sid)`             |
| 3 | Type        | `type.code`            | string       | codebook codes                        | codebook value                            |
| 4 | Condition   | `condition`            | string       | ICD-10 diagnose code(s) `[A-Z]\d{2}(?:\.\d+)?` (≤10),       | used verbatim (or concatenated with `+`)    |
| 5 | Sex         | `sex.code`             | string       | codebook codes                        | codebook value                            |
| 6 | Age Group   | `age_group.code`       | string       | codebook codes                        | codebook value                            |

### Stub format  
**Delimiter:** _(none)_

| # | Component        | Source field               | Type            | Pattern / Format            | Built from                               |
|--:|------------------|----------------------------|-----------------|-----------------------------|-------------------------------------------|
| 1 | Study stub       | `study.stub_code`          | string          | free string                 | codebook value (if present)               |
| 2 | Subject ID stub  | `subject_id`               | integer→Base62 | width 3 (default) — max 238,327        | 3-char Base62 from integer             |
| 3 | Type stub        | `type.stub_code`           | string          | 1 char                      | codebook value                            |
| 4 | Condition stub   | `condition`                | code→Base62    | N × 3-char Base62 stubs + 2-digit count (`%02d`)     | codebook order + 3-char Base62 from integer |
| 5 | Sex stub         | `sex.stub_code`            | string          | 1 char                      | codebook value                            |
| 6 | Age Group stub   | `age_group.stub_code`      | string          | 2 chars                     | codebook value                            |
