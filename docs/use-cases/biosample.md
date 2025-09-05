# Use Case II: Biosample-Level Encoding of GDC Data

## Data Download

On June 6, 2025, we downloaded biospecimen metadata for the project **TARGET-AML** from the [Genomic Data Commons (GDC)](https://gdc.cancer.gov/) portal as part of the archive:

```
biospecimen.project-target-aml.2025-06-29.tar.gz
```

All files were extracted to the `nb/data/biosample` directory:

```bash
cd nb/data/biosample
tar -xvf clinical.cohort.2025-06-02.tar.gz
```

The archive included the following four TSV files:

- `aliquot.tsv`
- `analyte.tsv`
- `portion.tsv`
- `sample.tsv`
- `slide.tsv`

We focused our analysis on `sample.tsv`, which contains:

- **39 columns**
- **4255 rows**

We will keep the files compressed to minimize space:

```bash
gzip *.tsv
```

---

## Data Pre-processing

We pre-processed the data using the script `../scripts/csv2_clarid_in.py`, along with a column mapping file:

??? example "View Mapping File"
    ```yaml
    --8<-- "../../nb/data/biosample/mapping_biosample.yaml"
    ```

Run the pre-processing with:

??? Hint "TSV UUID order"

    The script assumes that your data is sorted by UUID (cases.case_id) in this case.  If not, you need to sort it manually using a command like
     ```bash
     sort -t$'\t' -k1,1 raw.tsv > raw.sorted.tsv
     ```

```bash
../scripts/csv2_clarid_in.py \
    --entity biosample \
    -i sample.tsv.gz \
    -o sample_in.csv.gz \
    --mapping mapping_biosample.yaml
```

---

## ClarID encoding

### Human-Readable Format

```bash
../../../bin/clarid-tools code \
    --entity biosample \
    --format human \
    --action encode \
    --infile sample_in.csv.gz \
    --sep "," \
    --outfile clarid_human.csv.gz
```

### Stub Format

```bash
../../../bin/clarid-tools code \
    --entity biosample \
    --format stub \
    --action encode \
    --infile sample_in.csv.gz \
    --sep "," \
    --outfile clarid_stub.csv.gz
```

## ClarID decoding

### Human-Readable Format

```bash
../../../bin/clarid-tools code \
    --entity biosample \
    --format human \
    --action decode \
    --infile clarid_human.csv.gz \
    --sep "," \
    --outfile clarid_decoded_human.csv.gz
```

!!! Hint "Duplicated columns?"
    Note: The resulting columns will be appended to the right of the existing ones, which may result in some columns appearing duplicated.

### Stub Format

```bash
../../../bin/clarid-tools code \
    --entity biosample \
    --format stub \
    --action decode \
    --infile clarid_stub.csv.gz \
    --sep "," \
    --outfile clarid_decoded_stub.csv.gz
```

## Results Table

Below is an interactive table of the `human` format encodings. You can search (e.g. 'C92.0 Normal'), sort, and adjust the view to explore the data more easily. This is a [link](https://github.com/CNAG-Biomedical-Informatics/clarid-tools/tree/main/nb/data/biosample/clarid_human.csv.gz) to the actual file used.

<div class="datatable" markdown="1">
{{ read_csv('nb/data/biosample/clarid_human.csv.gz') }}
</div>

