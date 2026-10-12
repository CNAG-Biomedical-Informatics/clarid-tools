import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './index.module.css';

const identifierSegments = [
  {value: 'TCGA_AML', label: 'project'},
  {value: 'HomSap', label: 'species'},
  {value: '00001', label: 'subject'},
  {value: 'LIV', label: 'tissue'},
  {value: 'TUM', label: 'sample type'},
  {value: 'RNA', label: 'assay'},
  {value: 'I25.110', label: 'condition'},
  {value: 'CHL', label: 'timepoint'},
  {value: 'P1M', label: 'duration'},
] as const;

export default function Home(): React.ReactElement {
  const logo = useBaseUrl('/img/clarid-logo.png');
  const encodingFlow = useBaseUrl('/img/clarid-encoding-flow.svg');
  const pocketScreenshot = useBaseUrl('/img/clarid-pocket/biosample.png');

  return (
    <Layout
      title="ClarID-Tools"
      description="Reference implementation of the ClarID identifier specification">
      <main className={styles.page}>
        <section className={styles.hero}>
          <div className={styles.heroGrid}>
            <div className={styles.copy}>
              <p className={styles.kicker}>ClarID reference implementation</p>
              <h1>ClarID-Tools</h1>
              <p className={styles.claim}>
                Human-readable and compact identifiers for biomedical metadata
              </p>
              <p className={styles.lede}>
                A command-line implementation for encoding and decoding subject and
                biosample identifiers using versioned YAML codebooks and schema validation.
              </p>
              <div className={styles.actions}>
                <Link className={styles.primaryAction} to="/usage/quickstart">
                  Quickstart
                </Link>
                <Link className={styles.secondaryAction} to="/technical-details/specification">
                  Specification
                </Link>
                <a
                  className={styles.paperAction}
                  href="https://link.springer.com/article/10.1186/s13326-026-00349-6">
                  Published paper
                </a>
              </div>
            </div>
            <div className={styles.identityCard} aria-label="ClarID identifier example">
              <div className={styles.identityHeader}>
                <img className={styles.logo} src={logo} alt="" />
                <div>
                  <span>Illustrative biosample</span>
                  <strong>Human-readable format</strong>
                </div>
              </div>
              <code className={styles.identifier}>
                TCGA_AML-HomSap-00001-LIV-TUM-RNA-I25.110-CHL-P1M
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
              <p className={styles.sectionLabel}>Encoding model</p>
              <h2>From structured metadata to two identifier formats.</h2>
            </div>
            <p>
              ClarID-Tools validates the codebook and applies its mappings to generate
              human-readable and compact stub identifiers from the same input record.
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

        <section className={styles.pocketBand} aria-labelledby="clarid-pocket-heading">
          <Link className={styles.pocketBandVisual} to="/clarid-pocket" aria-label="View ClarID-Pocket">
            <img
              src={pocketScreenshot}
              alt="ClarID-Pocket showing the decoded fields of the illustrative biosample"
              width="1080"
              height="2400"
              loading="lazy"
            />
          </Link>
          <div className={styles.pocketBandCopy}>
            <p className={styles.sectionLabel}>Android companion</p>
            <h2 id="clarid-pocket-heading">Scan and decode ClarID labels on your phone</h2>
            <p>
              ClarID-Pocket reads subject and biosample QR labels offline using its bundled
              ClarID 0.04 codebook. The example shown is the same biosample illustrated above.
            </p>
            <div className={styles.pocketBandActions}>
              <Link to="/clarid-pocket">Explore ClarID-Pocket</Link>
              <a href="https://github.com/CNAG-Biomedical-Informatics/clarid-pocket/releases/latest">
                Download Android APK
              </a>
            </div>
          </div>
        </section>

        <section className={styles.section}>
          <p className={styles.sectionLabel}>Current scope</p>
          <div className={styles.sectionTitleRow}>
            <h2>Supported operations</h2>
            <p>Implemented for subject and biosample entities in the current release.</p>
          </div>
          <div className={styles.cardGrid}>
            <article className={styles.card}>
              <span>Encode</span>
              <h2>Generate identifiers</h2>
              <p>Map structured subject and biosample metadata to human or stub formats.</p>
            </article>
            <article className={styles.card}>
              <span>Decode</span>
              <h2>Recover encoded fields</h2>
              <p>Decode human-readable or stub identifiers back into structured values.</p>
            </article>
            <article className={styles.card}>
              <span>Validate</span>
              <h2>Check YAML codebooks</h2>
              <p>Validate codebook structure against the schema before processing data.</p>
            </article>
            <article className={styles.card}>
              <span>Process</span>
              <h2>Run table and QR workflows</h2>
              <p>Process individual records or CSV files and generate or decode QR codes.</p>
            </article>
          </div>
          <aside className={styles.scopeNote}>
            <strong>Scope</strong>
            <p>
              ClarID complements persistent identifiers and source metadata by carrying
              selected contextual fields. It is not intended to replace either.
            </p>
          </aside>
        </section>

        <section className={styles.pathSection}>
          <div>
            <p className={styles.sectionLabel}>Documentation</p>
            <h2>Guides, reference, and examples</h2>
            <p className={styles.pathIntro}>
              Start with a working command, inspect the CLI options, or browse example output.
            </p>
          </div>
          <div className={styles.pathList}>
            <Link to="/usage/quickstart">
              <span>Guide</span>
              <strong>Quickstart</strong>
              <small>Copy-paste commands for encoding and decoding.</small>
            </Link>
            <Link to="/usage/cli-reference">
              <span>Reference</span>
              <strong>CLI Reference</strong>
              <small>All commands, arguments, and output modes.</small>
            </Link>
            <Link to="/use-cases/subject">
              <span>Examples</span>
              <strong>Use Cases</strong>
              <small>Browsable GDC-derived subject and biosample examples.</small>
            </Link>
          </div>
        </section>
      </main>
    </Layout>
  );
}
