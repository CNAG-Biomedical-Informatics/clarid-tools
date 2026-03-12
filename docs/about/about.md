**ClarID-Tools** has been developed at [CNAG](https://cnag.eu), Barcelona, Spain.

## Scope

ClarID-Tools is the reference command-line implementation of the ClarID identifier approach described in the accompanying paper. In practice, the repository provides:

- encoding and decoding for `subject` and `biosample` identifiers
- YAML codebook support for controlled vocabularies and aliases
- JSON Schema validation for codebook structure
- example workflows based on GDC-derived datasets

## Relationship to the Paper

The paper describes the motivation, identifier design, and intended use in biomedical metadata integration.

This repository documents how that design is implemented operationally:

- the exact CLI behavior
- the configuration model used by the codebook
- practical encode/decode workflows
- reproducible examples and QR-code generation

If wording in the paper and implementation documentation ever diverge, the paper should be treated as the conceptual description and this documentation as the operational guide for the current software release.

## Developers

=== "CLI + Module"

    * [Manuel Rueda](https://github.com/mrueda)

=== "Documentation"

    * [Manuel Rueda](https://github.com/mrueda). 
      
    Project documentation was created using [Material for MkDocs](https://squidfunk.github.io/mkdocs-material).

## Acknowledgments

=== "CNAG"

    * [Ivo G. Gut](https://scholar.google.com/citations?user=YKdDEVYAAAAJ) and his [team](https://www.cnag.eu/teams/genome-research-unit/biomedical-genomics-group)
