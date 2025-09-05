# Use Case I: Subject-Level Encoding of GDC Data Cases

## Data Download

On June 1, 2025, we downloaded clinical metadata from the [Genomic Data Commons (GDC)](https://gdc.cancer.gov/) portal as part of the archive:

```
clinical.cohort.2025-06-02.tar.gz
```

All files were extracted to the `nb/data/subject` directory:

```bash
cd nb/data/subject
tar -xvf clinical.cohort.2025-06-02.tar.gz
```

The archive included the following four TSV files:

- `clinical.tsv`
- `family_history.tsv`
- `follow_up.tsv`
- `pathology_detail.tsv`

We focused our analysis on `clinical.tsv`, which contains:

- **210 columns**
- **113,760 rows**
- Data from **86 studies**, including **33 from TCGA**

Note that multiple cases can share the same UUID.

We will keep the files compressed to minimize space:

```bash
gzip *.tsv
```

---

## Data Pre-processing

We pre-processed the data using the script `../scripts/csv2_clarid_in.py`, along with a column mapping file:

??? example "View Mapping File"
    ```yaml
    --8<-- "../nb/data/subject/mapping_subject.yaml"
    ```

Run the pre-processing with:

??? Hint "TSV UUID order"

    The script assumes that your data is sorted by UUID (cases.case_id) in this case.  If not, you need to sort it manually using a command like
     ```bash
     sort -t$'\t' -k1,1 raw.tsv > raw.sorted.tsv
     ```


```bash
../scripts/csv2_clarid_in.py \
    --entity subject \
    -i clinical.tsv.gz \
    -o clinical_in.csv.gz \
    --mapping mapping_subject.yaml
```

---

## ClarID encoding

### Human-Readable Format

```bash
../../../bin/clarid-tools code \
    --entity subject \
    --format human \
    --action encode \
    --infile clinical_in.csv.gz \
    --sep "," \
    --outfile clarid_human.csv.gz
```

### Stub Format

```bash
../../../bin/clarid-tools code \
    --entity subject \
    --format stub \
    --action encode \
    --infile clinical_in.csv.gz \
    --sep "," \
    --outfile clarid_stub.csv.gz
```

## ClarID decoding

### Human-Readable Format

```bash
../../../bin/clarid-tools code \
    --entity subject \
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
    --entity subject \
    --format stub \
    --action decode \
    --infile clarid_stub.csv.gz \
    --sep "," \
    --outfile clarid_decoded_stub.csv.gz
```


## Results Table

Below is an interactive table of the `human` format encodings (displaying first 10K rows). You can search (e.g., 'C02.9 Female'), sort, and adjust the view to explore the data more easily. This is a [link](https://github.com/CNAG-Biomedical-Informatics/clarid-tools/tree/main/nb/data/subject/clarid_human.csv.gz) to the actual file used.

<div class="datatable" markdown="1">
{{ read_csv('nb/data/subject/clarid_human.csv.gz', nrows=10000) }}
</div>

