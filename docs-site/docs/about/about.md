# About ClarID-Tools

**ClarID-Tools** is developed at [CNAG](https://cnag.eu), Barcelona, Spain, as
the reference command-line implementation of the ClarID identifier approach.

## Scope

<div class="claridAboutGrid">
  <article>
    <span>Identifiers</span>
    <h3>Subject and biosample IDs</h3>
    <p>Encoding and decoding for the two ClarID entity types currently implemented by the toolkit.</p>
  </article>
  <article>
    <span>Codebooks</span>
    <h3>Controlled vocabularies</h3>
    <p>YAML codebook support for labels, aliases, compact stubs, and project-specific vocabulary choices.</p>
  </article>
  <article>
    <span>Validation</span>
    <h3>Schema-backed checks</h3>
    <p>JSON Schema validation for codebook structure before identifiers are generated or decoded.</p>
  </article>
  <article>
    <span>Examples</span>
    <h3>Operational workflows</h3>
    <p>Reproducible command-line examples, QR-code workflows, and GDC-derived use cases.</p>
  </article>
</div>

In short: the paper defines the concept; this repository shows how to run it.

## Relationship to the Paper

<div class="claridAboutCallout">
  <p>
    The paper describes the motivation, identifier design, and intended use in
    biomedical metadata integration. This documentation describes the operational
    implementation for the current software release.
  </p>
</div>

This includes the exact CLI behavior, the codebook configuration model,
practical encode/decode workflows, reproducible examples, and QR-code
generation.

If wording in the paper and implementation documentation ever diverge, the paper should be treated as the conceptual description and this documentation as the operational guide for the current software release.

## Development

ClarID-Tools is developed and maintained by
[Manuel Rueda](https://github.com/mrueda) at CNAG.

## Acknowledgments

ClarID-Tools was developed with support from
[Ivo G. Gut](https://scholar.google.com/citations?user=YKdDEVYAAAAJ) and the
[Genome Research Unit Biomedical Genomics Group](https://www.cnag.eu/teams/genome-research-unit/biomedical-genomics-group)
at CNAG.
