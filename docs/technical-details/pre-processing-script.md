# Pre-processing Script

Before encoding with ClarID-Tools, raw metadata often need normalization. This is especially relevant for `condition`, because ClarID-Tools expects ICD-10 diagnosis codes rather than free-text disease labels.

If your source data contain free text, project-specific labels, or mixed delimiters, convert them to the expected ICD-10 representation during pre-processing.

!!! note "About `condition`"
    ClarID-Tools expects `condition` values in ICD-10 form before encoding. In bulk workflows, the pre-processing script is the recommended place to normalize free-text or project-specific disease labels into ICD-10 codes.

--8<-- "../tools/csv/README.md"
