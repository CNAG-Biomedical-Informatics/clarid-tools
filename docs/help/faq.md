# Frequently Asked Questions

## Codebook

??? Example "How do you perform the Base62 encoding for `species`"

    Below is a small Python example that generates the 2-character Base62 encoding space used for `species`.

    ```python
     #!/usr/bin/env python3
    import sys

    ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    BASE = len(ALPHABET)  # 62
    MAX_VALUE = BASE ** 2  # 3844

    def encode_base62(num: int) -> str:
        """
        Encode an integer in the range [0, 3843] to a 2-character Base62 string.
        """
        if not (0 <= num < MAX_VALUE):
            raise ValueError(f'Number out of range (0 ≤ num < {MAX_VALUE}), got {num}')
        high = num // BASE
        low = num % BASE
        return ALPHABET[high] + ALPHABET[low]

    def main():
        for n in range(MAX_VALUE):
            print(f'{n}\t{encode_base62(n)}')

    if __name__ == '__main__':
        main()
    ```

    ##### last change 2025-08-01 by Manuel Rueda [:fontawesome-brands-github:](https://github.com/mrueda)

??? question "Why do the `species` and `subject_id` parts of stub IDs not look like the human-readable version?"

    Because they are encoded independently for compactness.

    * `species` uses a static 2-character `stub_code` from the YAML codebook
    * `subject_id` is converted from the numeric subject identifier into fixed-width Base62

    Stub fields therefore represent the same metadata as the human-readable form, but they are not character-by-character abbreviations of it.


??? question "For `condition` do I need to encode to ICD-10 before ClarID-Tools?"

    Yes, ClarID-Tools reads ICD-10 diagnosis codes. Take a look at [this documentation](../technical-details/pre-processing-script.md).

    ##### last change 2025-07-21 by Manuel Rueda [:fontawesome-brands-github:](https://github.com/mrueda)

??? question "Can I include multiple ICD-10 diagnosis codes?"

    Yes. 

    * Command-line: `--condition C22.1,C22.2` (comma separated)
    * Bulk (CSV): Separate them by `;` (semicolon) 

    The maximum is set with the parameter `--max_conditions`, which defaults to **10**. We reserve 2 chars for that field, so the limit is 99 conditions.

    ##### last change 2025-08-10 by Manuel Rueda [:fontawesome-brands-github:](https://github.com/mrueda)

??? question "Does the stub `condition` encoding depend on the YAML order?"

    No. In the current reference implementation, stub `condition` values are derived from the packaged ICD-10 order map distributed with ClarID-Tools.

    In practice, encoded values should be interpreted together with the ClarID-Tools release and associated resources used for encoding. Future revisions may revisit this mapping strategy if broader interoperability needs emerge.

??? question "What is the difference between `--subject_id_pad_length` and `--subject_id_base62_width`?"

    They control different formats of the same `subject_id` field.

    * `--subject_id_pad_length` controls decimal zero-padding in human-readable IDs
    * `--subject_id_base62_width` controls the width of the Base62 field in stub IDs

    Example:

    * human format: `subject_id = 42` with pad length 5 becomes `00042`
    * stub format: `subject_id = 42` with Base62 width 3 becomes a 3-character Base62 stub

??? question "Which ICD-10 code should I use when no specific disease is available?"

    Since we rely on ICD-10 coding, we have selected code Z00.00 ("Encounter for general adult medical examination without abnormal findings").

    If you believe there is a more appropriate code for this context, please feel free to suggest it.

    ##### last change 2025-08-10 by Manuel Rueda [:fontawesome-brands-github:](https://github.com/mrueda)

## Usage and Troubleshooting

??? question "When should I use `human` format versus `stub` format?"

    Use `human` format when the identifier will be inspected directly by people.

    Use `stub` format when you need a compact identifier for labels, QR codes, filenames, or systems with tighter space constraints.

??? question "What if my project needs more species than the current stub format allows?"

    The current 2-character Base62 `species` stub design supports up to 3,844 values. This is typically sufficient for biomedical metadata integration, which is the primary target of ClarID-Tools.

    If your project exceeds that range, the recommended options are:

    * use the human-readable format
    * adopt an extended stub specification for your project

    A wider `species` stub field is a specification-level change, not just a codebook update, because it affects interoperability.

??? question "Why do I see duplicated columns after decoding a CSV file?"

    In bulk decode mode, ClarID-Tools appends decoded fields to the right of the existing input table. If the source table already contains some of those columns, they will appear duplicated in the output.

??? question "What are the most common reasons encoding fails?"

    The most common causes are:

    * a metadata value is missing from the YAML codebook
    * the wrong input separator was used
    * the `condition` value is malformed or not normalized as expected
    * a required field for the selected entity or format is missing

??? question "What are the most common reasons decoding fails?"

    The most common causes are:

    * `--clar_id` or `--stub_id` was not provided in single-record mode
    * the wrong format was selected for the identifier being decoded
    * a bulk input file does not contain the expected ID column
    * the codebook used for decoding does not match the one used for encoding

## General

??? question "What are the benefits of ClarID for biomedical research?"

    ClarID is particularly useful in biomedicine because it fills the gap between rich metadata schemas and traditional opaque accession numbers. The structured identifiers enhance traceability and facilitate downstream data analysis by embedding important context directly into the ID. 

    ##### last change 2025-10-14 by Manuel Rueda [:fontawesome-brands-github:](https://github.com/mrueda)

??? question "How do I cite `clarid-tools`?"

    You can cite the **ClarID-Tools** paper.

    !!! Note "Citation"
        Manuel Rueda and Ivo G. Gut (2025). ClarID: A Human-Readable and Compact Identifier Specification for Biomedical Metadata Integration. _Submitted_.

    ##### last change 2025-08-10 by Manuel Rueda [:fontawesome-brands-github:](https://github.com/mrueda)

??? question "Should the documentation be updated when the paper goes live?"

    Yes. The citation string should be updated consistently across the documentation site, the repository `README`, and any notebooks or example material released with the paper.
