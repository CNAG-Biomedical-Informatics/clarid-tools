<p align="center">
  <a href=""><img src="img/clarid-logo.png" width="200" alt="ClarID-Tools"></a>
</p>

<div align="center">
<strong>Welcome to the documentation for ClarID-Tools</strong>
</div>

{% include-markdown "../README.md" start="<!--description-start-->" end="<!--description-end-->" %}

## Before You Start

Choose the command style that matches how you are using ClarID-Tools:

- If you cloned this repository, run commands from the repository root with `bin/clarid-tools`.
- If you installed ClarID-Tools system-wide or with CPAN, run `clarid-tools`.
- You can omit `--codebook` unless you want to use a custom codebook. The packaged default codebook is used automatically.
- The `qrcode` subcommand requires external tools:
  - host install or git checkout: install `qrencode` and `zbarimg` (`zbar-tools`)
  - Docker image: these tools are already included

## Start Here

If you are new to ClarID-Tools, use this order:

1. Read the [Quickstart](usage/quickstart.md) for copy-paste examples.
2. Check the [CLI Reference](usage/cli-reference.md) for all command options.
3. Review the [Specification](technical-details/specification.md) if you need the exact identifier structure.
4. See the [Use Cases](use-cases/subject.md) and [Use Cases](use-cases/biosample.md) for real GDC-derived examples.

## Choosing an ID Format

Use `human` format when the identifier will be read directly by people in reports, spreadsheets, filenames, or manual review workflows.

Use `stub` format when compactness matters more than readability, for example in QR codes, labels, or constrained downstream systems.

Both formats are generated from the same metadata and codebook, so you can encode and decode between structured metadata and IDs consistently.

## What This Repository Implements

The ClarID paper defines the identifier concept and rationale. This repository provides the reference command-line implementation, the codebook/schema validation workflow, and end-to-end examples for `subject` and `biosample` identifiers.
