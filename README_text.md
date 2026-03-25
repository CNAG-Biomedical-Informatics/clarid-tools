# ClarID-Tools

<!--description-start-->

## 📝 Description

**ClarID-Tools** is a toolkit for working with the **ClarID** specification, including the reference command-line implementation, preprocessing utilities, and example workflows. The objective is to standardize how subject and biosample metadata are transformed into compact, informative IDs for downstream integration, tracking, and exchange.

---

## 🔬 Key Features

- 🧬 **Biosample and Subject ID generation** from structured metadata
- 🩺 **Support for clinical and experimental metadata**, including species, tissue, assay, condition, and more
- 📄 **Human-readable and stub-formatted modes** for compact or verbose identifiers
- 🧪 **Bulk and single-record encoding/decoding**
- ✅ **Schema validation** using JSON Schema and YAML codebooks
- 📦 Command-line interface 

---

<!--description-end-->

## 🚀 Getting Started

### 🛠️  Installation

We offer two modes of installation:

1. [Non-Containerized](non-containerized/README.md)


2. [Containerized](docker/README.md)


### ▶️ Running the CLI

- If you cloned this repository, run commands from the repository root with `bin/clarid-tools`.
- If you installed ClarID-Tools with CPAN or system-wide, run `clarid-tools`.
- The packaged default codebook is used automatically, so `--codebook` is only needed when you want to use a custom codebook.
- The `qrcode` subcommand requires `qrencode` and `zbarimg` on host installs. The Docker image already includes them.

### 📘 Example Usage

1. [Quickstart](https://cnag-biomedical-informatics.github.io/clarid-tools/usage/quickstart/)

2. Use Cases:
 
  * [Biosample](https://cnag-biomedical-informatics.github.io/clarid-tools/use-cases/biosample/)
  * [Subject](https://cnag-biomedical-informatics.github.io/clarid-tools/use-cases/subject/)

---

## 🧠 Citation

If you use **ClarID-Tools** in your work, please cite:

Manuel Rueda and Ivo G. Gut (2025). ClarID: A Human-Readable and Compact Identifier Specification for Biomedical Metadata Integration. _Journal of Biomedical Semantics_. Accepted.

---


## 👤 Author 

Written by Manuel Rueda, PhD. Info about CNAG can be found at [https://www.cnag.eu](https://www.cnag.eu).

---


## 📄 License

ClarID-Tools is released under the Artistic License. See the [LICENSE](LICENSE) file for details.
