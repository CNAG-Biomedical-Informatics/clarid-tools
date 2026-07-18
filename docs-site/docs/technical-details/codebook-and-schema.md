# 📘 Codebook and Schema

The ClarID YAML codebook maps project vocabulary to the values used in
human-readable and stub identifiers. The bundled JSON Schema checks its
structure before ClarID-Tools encodes or decodes data.

## Reference Files

| Resource | Stable path | Purpose |
|---|---|---|
| Reference codebook | `share/clarid-codebook.yaml` | Default vocabulary and encoding values |
| JSON Schema | `share/clarid-codebook-schema.json` | Structural validation rules |
| Versioned resources | `share/versions/<release>/` | Release-pinned codebooks and schemas |

The stable paths are relative symbolic links to the resources shipped for the
latest ClarID release. The files can also be inspected directly in the
repository:

- [Reference codebook](https://github.com/CNAG-Biomedical-Informatics/clarid-tools/blob/main/share/clarid-codebook.yaml)
- [JSON Schema](https://github.com/CNAG-Biomedical-Informatics/clarid-tools/blob/main/share/clarid-codebook-schema.json)
- [Versioned resources](https://github.com/CNAG-Biomedical-Informatics/clarid-tools/tree/main/share/versions)

Validate a codebook before using it in a workflow:

```bash
clarid-tools validate --codebook share/clarid-codebook.yaml
```

## 📝 Metadata

The metadata section records the ClarID release and the provenance of a
codebook:

```yaml
metadata:
  version: "0.04"                    # Official ClarID release
  local_version: "CNAG-GDC-v1"      # Project revision (optional)
  author: "M. Rueda"
  center: "CNAG"
  date: "2026-04-01"                 # YYYY-MM-DD
  description: "ClarID codebook"
  repository: "https://github.com/cnag-biomedical-informatics/clarid-tools"
```

`version` identifies the official ClarID specification release targeted by the
codebook. ClarID-Tools uses this value for compatibility checks.

`local_version` distinguishes project-specific codebook revisions that retain
the same ClarID structure but change controlled vocabularies, aliases, or local
dictionary values.

:::note[Schema version]
Compatibility is checked against `metadata.version` in the codebook, not
`schemaVersion` in the JSON Schema. The schema `$id` follows the ClarID release,
while `schemaVersion` changes only when the validation rules change. It may
therefore retain an earlier value across ClarID releases.
:::

## 🌐 Entities

All encoding vocabulary lives under `entities`. Global fall-through entries
provide explicit values for unknown or unavailable metadata:

```yaml
entities:
  _defaults: &defaults
    "Unknown":
      code: UNK
      stub_code: U
      label: "Unknown"
      id: "NCIT:C17998"
    "Not Available":
      code: NAV
      stub_code: n
      label: "Not Available"
      id: "NCIT:C126101"
```

Each vocabulary key is an accepted input value. `code` is used in the
human-readable identifier, `stub_code` in the compact identifier, `label` for
display, and `id` for an external ontology or terminology reference.

## 🧬 Biosample

### Project

The reference codebook anchors the project map so that subject `study` entries
can reuse it:

```yaml
entities:
  biosample:
    project: &all_projects
      "TCGA-AML":
        code: TCGA_AML
        stub_code: AML
        label: "TCGA Acute Myeloid Leukemia"
        id: "NCIT:C17998"
```

### Species

```yaml
entities:
  biosample:
    species:
      Human:
        code: HomSap
        stub_code: "01"
        label: "Homo sapiens"
        id: "NCBITaxon:9606"
        tax_code: MPH
```

<details>
<summary>Species code convention</summary>

The reference vocabulary follows the convention described by Schrade et al. in
*Animals* (2024), Table 2:

- `tax_code` is a three-letter class, order, and family classification, such as
  `MPC` for Mammalia, Primates, and Cercopithecidae.
- `code` is a six-letter binomial acronym formed from three letters of the genus
  and three letters of the species, such as `MacMul` for *Macaca mulatta*.
- `stub_code` is a static compact species value defined by the codebook. The
  reference codebook uses two characters, such as `01` for *Homo sapiens*.

`tax_code` is retained as metadata and is not used by the encoder or decoder.
Species stub codes must use a consistent width within a codebook.

</details>

### Tissue

```yaml
entities:
  biosample:
    tissue:
      Liver:
        code: LIV
        stub_code: L
        label: "Liver"
        id: "UBERON:0002107"
```

### Sample Type

```yaml
entities:
  biosample:
    sample_type:
      Tumor:
        code: TUM
        stub_code: T
        label: "Tumor"
        id: "NCIT:C4872"
```

### Assay

```yaml
entities:
  biosample:
    assay:
      RNA_seq:
        code: RNA
        stub_code: R
        label: "RNA-seq"
        id: "EFO:0008896"
```

### Timepoint

```yaml
entities:
  biosample:
    timepoint:
      Baseline:
        code: BSL
        stub_code: B
        label: "Baseline"
        id: "NCIT:C25213"
```

### Pattern-Based Fields

Patterns validate values that are not selected from a vocabulary map and define
their human and stub formatting:

```yaml
entities:
  biosample:
    condition_pattern: &condition_pattern
      regex: '^([A-Z]\d{2}(?:\.\d+)?)$'
      code_format: '%s'
      stub_format: '%s'

    duration_pattern:
      regex: '^(?:P?(\d)([DWMY])|P?(0)(N))$'
      code_format: 'P%d%s'
      stub_format: '%d%s'

    batch_pattern:
      regex: '^(\d{1,2})$'
      code_format: 'B%02d'
      stub_format: 'B%02d'

    replicate_pattern:
      regex: '^(\d{1,2})$'
      code_format: 'R%02d'
      stub_format: 'R%02d'
```

The duration pattern intentionally accepts a single digit and one unit, or
`P0N`. See the [Specification](./specification.md) for the resulting identifier
fields.

## 👤 Subject

The reference codebook reuses the project map as `study` and the biosample
condition pattern through YAML aliases:

```yaml
entities:
  subject:
    study: *all_projects
    condition_pattern: *condition_pattern
```

Subject-specific controlled vocabularies use the same entry structure:

```yaml
entities:
  subject:
    type:
      Case:
        code: Case
        stub_code: C
        label: "Case Study"
        id: "NCIT:C15362"

    sex:
      Male:
        code: Male
        stub_code: M
        label: "Male"
        id: "PATO:0000384"

    age_group:
      Age20to29:
        code: A20_29
        stub_code: A2
        label: "Age 20-29"
        id: "APOLLO:SV_00000241"
```

## Project-Specific Codebooks

1. Copy the codebook associated with the ClarID release used by your software.
2. Keep `metadata.version` unchanged and set a meaningful `local_version`.
3. Add or edit vocabulary entries without changing the required hierarchy.
4. Validate the resulting file.
5. Pass it through `--codebook` when encoding or decoding.

```bash
cp share/versions/0.04/clarid-codebook.yaml project-codebook.yaml
clarid-tools validate --codebook project-codebook.yaml
clarid-tools code \
  --codebook project-codebook.yaml \
  --entity biosample \
  --action encode \
  --format human \
  --infile project-input.csv
```

:::warning[Keep codebooks with generated identifiers]
ClarID identifiers store the mapped `code` or `stub_code`, not the original
vocabulary key. If a mapping changes, the same input metadata can produce a
different identifier, and identifiers created previously may no longer decode
correctly with the revised codebook. Keep the codebook used for encoding under
version control and record its `local_version` with the corresponding data or
workflow.
:::

## Naming Conventions

- Vocabulary keys generally use CamelCase, such as `RhesusMacaque` and
  `PeripheralBlood`.
- Attributes use snake_case, such as `stub_code` and `tax_code`.
- Established values such as `RNA_seq` and `Not Available` retain their
  spelling for compatibility.
- Codes already used in identifiers should not be reassigned to a different
  meaning.
