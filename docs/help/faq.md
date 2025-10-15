# Frequently Asked Questions

## Codebook 

??? Example "How do you perform the Base62 encoding for `species`"

    See below an example of a Python code to create the encoding for species

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


??? question "For `condition` do I need to encode to ICD-10 before ClariD-Tools?"

    Yes, Clarid-Tools reads ICD-10 diagnoses codes. Take look to [this documentation](../technical-details/pre-processing-script.md)).

    ##### last change 2025-07-21 by Manuel Rueda [:fontawesome-brands-github:](https://github.com/mrueda)

??? question "Can I include multiple ICD-10 diagnose codes?"

    Yes. 

    * Command-line: `--condition C22.1,C22.2` (comma separated)
    * Bulk (CSV): Separate them by `;` (semicolon) 

    The maximum is set with the parameter `--max-conditions` that defaults to **10**. We reserve 2 chars for that field so the limit will be 99 conditions.

    ##### last change 2025-08-10 by Manuel Rueda [:fontawesome-brands-github:](https://github.com/mrueda)

??? question "Which ICD-10 code should I use when no specific disease is available?"

    Since we rely on ICD-10 coding, we have selected code Z00.00 ("Encounter for general adult medical examination without abnormal findings").

    If you believe there's a more appropriate code for this context, please feel free to suggest it :smile:.

    ##### last change 2025-08-10 by Manuel Rueda [:fontawesome-brands-github:](https://github.com/mrueda)

## General 

??? question "What are the benefits of ClarID for biomedical research?"

    ClarID is particularly useful in biomedicine because it fills the gap between rich metadata schemas and traditional opaque accession numbers. The structured identifiers enhance traceability and facilitate downstream data analysis by embedding important context directly into the ID. 

    ##### last change 2025-10-14 by Manuel Rueda [:fontawesome-brands-github:](https://github.com/mrueda)

??? question "How do I cite `clarid-tools`?"

    You can cite the **Clarid-Tools** paper. Thx!

    !!! Note "Citation"
        Manuel Ruedan and Ivo G. Gut (2025). ClarID: A Human-Readable and Compact Identifier Specification for Biomedical Metadata Integration. _Submitted_.

    ##### last change 2025-08-10 by Manuel Rueda [:fontawesome-brands-github:](https://github.com/mrueda)
