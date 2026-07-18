import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './index.module.css';

const identifierSegments = [
  {value: 'CNAG_Test', label: 'project'},
  {value: 'HomSap', label: 'species'},
  {value: '00042', label: 'subject'},
  {value: 'LIV', label: 'tissue'},
  {value: 'TUM', label: 'sample type'},
  {value: 'RNA', label: 'assay'},
  {value: 'C15.3', label: 'condition'},
  {value: 'TRT', label: 'timepoint'},
  {value: 'P1M', label: 'duration'},
] as const;

export default function Home(): React.ReactElement {
  const logo = useBaseUrl('/img/clarid-logo.png');
  const encodingFlow = useBaseUrl('/img/clarid-encoding-flow.svg');

  return (
    <Layout
      title="ClarID-Tools"
      description="Human-readable identifiers for biomedical metadata">
      <main className={styles.page}>
        <section className={styles.hero}>
          <div className={styles.heroGrid}>
            <div className={styles.copy}>
              <p className={styles.kicker}>ClarID-Tools</p>
              <h1>Human-readable identifiers for biomedical metadata</h1>
              <p className={styles.lede}>
                Encode and decode subject and biosample identifiers with a versioned
                codebook, schema validation, and reproducible command-line workflows.
              </p>
              <div className={styles.actions}>
                <Link className={styles.primaryAction} to="/usage/quickstart">
                  Quickstart
                </Link>
                <Link className={styles.secondaryAction} to="/technical-details/specification">
                  Read the specification
                </Link>
              </div>
            </div>
            <div className={styles.identityCard} aria-label="ClarID identifier example">
              <div className={styles.identityHeader}>
                <img className={styles.logo} src={logo} alt="" />
                <div>
                  <span>Biosample example</span>
                  <strong>Nine fields, one identifier</strong>
                </div>
              </div>
              <code className={styles.identifier}>
                CNAG_Test-HomSap-00042-LIV-TUM-RNA-C15.3-TRT-P1M
              </code>
              <div className={styles.segmentGrid}>
                {identifierSegments.map((segment) => (
                  <div key={segment.label}>
                    <code>{segment.value}</code>
                    <span>{segment.label}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        <section className={styles.flowSection}>
          <div className={styles.flowHeading}>
            <div>
              <p className={styles.sectionLabel}>From metadata to identifiers</p>
              <h2>One encoding workflow, two useful forms.</h2>
            </div>
            <p>
              ClarID-Tools applies explicit codebook mappings and schema checks before
              generating a readable identifier and its compact stub from the same input.
            </p>
          </div>
          <figure className={styles.diagramFrame}>
            <div className={styles.diagramScroller}>
              <img
                src={encodingFlow}
                alt="Structured biosample metadata and a validated codebook entering ClarID-Tools and producing human-readable and stub identifiers"
              />
            </div>
            <figcaption>
              The codebook keeps project vocabulary explicit; the CLI applies it consistently
              to individual records and bulk tables.
            </figcaption>
          </figure>
        </section>

        <section className={styles.section}>
          <p className={styles.sectionLabel}>What it does</p>
          <div className={styles.sectionTitleRow}>
            <h2>A focused toolkit for the identifier lifecycle.</h2>
            <p>Use the same command-line interface from first encoding through validation and reuse.</p>
          </div>
          <div className={styles.cardGrid}>
            <article className={styles.card}>
              <span>01 / Encode</span>
              <h2>Generate ClarID identifiers</h2>
              <p>Create subject and biosample IDs from structured metadata fields.</p>
            </article>
            <article className={styles.card}>
              <span>02 / Decode</span>
              <h2>Recover metadata</h2>
              <p>Decode human-readable or stub IDs back into tabular values.</p>
            </article>
            <article className={styles.card}>
              <span>03 / Validate</span>
              <h2>Use schema-backed codebooks</h2>
              <p>Validate YAML codebooks while keeping project vocabularies explicit.</p>
            </article>
            <article className={styles.card}>
              <span>04 / Scale</span>
              <h2>Run bulk workflows</h2>
              <p>Use the same CLI for single records, CSV batches, QR codes, and examples.</p>
            </article>
          </div>
        </section>

        <section className={styles.pathSection}>
          <div>
            <p className={styles.sectionLabel}>Start here</p>
            <h2>Choose the documentation you need.</h2>
            <p className={styles.pathIntro}>
              Start with a working command, inspect every option, or browse real output.
            </p>
          </div>
          <div className={styles.pathList}>
            <Link to="/usage/quickstart">
              <span>01</span>
              <strong>Quickstart</strong>
              <small>Copy-paste commands for encoding and decoding.</small>
            </Link>
            <Link to="/usage/cli-reference">
              <span>02</span>
              <strong>CLI Reference</strong>
              <small>All commands, arguments, and output modes.</small>
            </Link>
            <Link to="/use-cases/subject">
              <span>03</span>
              <strong>Use Cases</strong>
              <small>Browsable GDC-derived subject and biosample examples.</small>
            </Link>
          </div>
        </section>
      </main>
    </Layout>
  );
}
