# ClarID-Tools Documentation

This page is the map for the ClarID-Tools documentation. Use it to decide where
to start, which command style applies to your setup, and when to use each ID
format.

ClarID-Tools is the reference command-line implementation for encoding and
decoding `subject` and `biosample` identifiers from structured biomedical
metadata.

## Before You Start

<div class="claridNotePanel">
  <p><strong>Pick the command style that matches your setup.</strong></p>
  <ul>
    <li>If you cloned this repository, run commands from the repository root with <code>bin/clarid-tools</code>.</li>
    <li>If you installed ClarID-Tools system-wide or with CPAN, run <code>clarid-tools</code>.</li>
    <li>You can omit <code>--codebook</code> unless you want to use a custom codebook. The packaged default codebook is used automatically.</li>
    <li>The <code>qrcode</code> subcommand needs <code>qrencode</code> and <code>zbarimg</code>; the Docker image already includes them.</li>
  </ul>
</div>

## Start Here

<div class="claridPath">
  <a href="../usage/quickstart">
    <span>01</span>
    <strong>Quickstart</strong>
    <small>Copy-paste examples for encoding and decoding.</small>
  </a>
  <a href="../usage/cli-reference">
    <span>02</span>
    <strong>CLI Reference</strong>
    <small>All commands, options, and output modes.</small>
  </a>
  <a href="../technical-details/specification">
    <span>03</span>
    <strong>Specification</strong>
    <small>The exact identifier structure and supported fields.</small>
  </a>
  <a href="../use-cases/subject">
    <span>04</span>
    <strong>Use Cases</strong>
    <small>Browsable GDC-derived subject and biosample examples.</small>
  </a>
</div>

## What You Can Do

- Encode subject and biosample identifiers from structured metadata.
- Decode human-readable or stub identifiers back into tabular values.
- Validate YAML codebooks against the bundled JSON Schema.
- Run single-record, bulk CSV, QR-code, and preprocessing workflows from the CLI.

## Choosing an ID Format

<div class="claridSplit">
  <div>
    <h3><code>human</code></h3>
    <p>Use this when identifiers will be read directly by people in reports, spreadsheets, filenames, or manual review workflows.</p>
  </div>
  <div>
    <h3><code>stub</code></h3>
    <p>Use this when compactness matters more than readability, for example in QR codes, labels, or constrained downstream systems.</p>
  </div>
</div>

Both formats are generated from the same metadata and codebook, so you can encode and decode between structured metadata and IDs consistently.

## What This Repository Implements

The ClarID paper defines the identifier concept and rationale. This repository provides the reference command-line implementation, the codebook/schema validation workflow, and end-to-end examples for `subject` and `biosample` identifiers.
