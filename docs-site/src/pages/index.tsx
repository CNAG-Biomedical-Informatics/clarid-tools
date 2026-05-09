import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './index.module.css';

export default function Home(): React.ReactElement {
  const logo = useBaseUrl('/img/clarid-logo.png');

  return (
    <Layout
      title="ClarID-Tools"
      description="Human-readable and compact identifiers for biomedical metadata">
      <main className={styles.page}>
        <section className={styles.hero}>
          <div className={styles.heroGrid}>
            <div className={styles.copy}>
            <p className={styles.kicker}>ClarID-Tools</p>
            <h1>Human-readable and compact identifiers for biomedical metadata</h1>
            <p className={styles.lede}>
              Encode and decode subject and biosample identifiers with a versioned
              codebook, schema validation, and reproducible command-line workflows.
            </p>
            <div className={styles.actions}>
              <Link className="button button--primary button--lg" to="/usage/quickstart">
                Quickstart
              </Link>
              <Link className="button button--secondary button--lg" to="/technical-details/specification">
                Specification
              </Link>
            </div>
          </div>
            <div className={styles.identityCard} aria-label="ClarID identifier example">
              <img className={styles.logo} src={logo} alt="ClarID-Tools" />
              <div className={styles.identifier}>
                CNAG_Test-HomSap-00042-LIV-TUM-RNA-C15.3-TRT-P1M
              </div>
              <div className={styles.tokens}>
                <span>project</span>
                <span>species</span>
                <span>subject</span>
                <span>tissue</span>
                <span>condition</span>
              </div>
            </div>
          </div>
        </section>

        <section className={styles.section}>
          <p className={styles.sectionLabel}>What it does</p>
          <div className={styles.cardGrid}>
            <article className={styles.card}>
              <span>Encode</span>
              <h2>Generate ClarID identifiers</h2>
              <p>Create subject and biosample IDs from structured metadata fields.</p>
            </article>
            <article className={styles.card}>
              <span>Decode</span>
              <h2>Recover metadata</h2>
              <p>Decode human-readable or stub IDs back into tabular values.</p>
            </article>
            <article className={styles.card}>
              <span>Validate</span>
              <h2>Use schema-backed codebooks</h2>
              <p>Validate YAML codebooks while keeping project vocabularies explicit.</p>
            </article>
            <article className={styles.card}>
              <span>Scale</span>
              <h2>Run bulk workflows</h2>
              <p>Use the same CLI for single records, CSV batches, QR codes, and examples.</p>
            </article>
          </div>
        </section>

        <section className={styles.pathSection}>
          <div>
            <p className={styles.sectionLabel}>Start here</p>
            <h2>Pick the shortest path into the docs.</h2>
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
