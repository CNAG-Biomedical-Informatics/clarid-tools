# ClarID-Tools Docusaurus Site

## Development

```bash
npm install
npm run start
npm run build
npm run typecheck
```

Some Docusaurus pages are generated from repository README files to avoid manual duplication.

Source files:

- `../non-containerized/README.md` -> `docs/download-and-installation/non-containerized.md`
- `../docker/README.md` -> `docs/download-and-installation/docker-based.md`
- `../utils/csv/README.md` -> `docs/technical-details/pre-processing-script.md`

Edit the source README, not the generated Docusaurus page, then run:

```bash
npm run sync:readmes
```

`npm run start` and `npm run build` run the sync automatically.
