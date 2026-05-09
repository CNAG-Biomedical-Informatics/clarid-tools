import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

const config: Config = {
  title: 'ClarID-Tools Documentation',
  tagline: 'Human-readable and compact identifiers for biomedical metadata',
  favicon: 'img/clarid-logo.png',
  url: 'https://cnag-biomedical-informatics.github.io',
  baseUrl: '/clarid-tools/',
  organizationName: 'CNAG-Biomedical-Informatics',
  projectName: 'clarid-tools',
  onBrokenLinks: 'throw',
  onBrokenAnchors: 'throw',
  markdown: {
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'throw',
    },
  },
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },
  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: '/',
          remarkPlugins: [remarkMath],
          rehypePlugins: [rehypeKatex],
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],
  themes: ['@docusaurus/theme-mermaid'],
  stylesheets: [
    {
      href: 'https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/katex.min.css',
      type: 'text/css',
      integrity: 'sha384-5TcZemv2l/9On385z///+d7MSYlvIEw9FuZTIdZ14vJLqWphw7e7ZPuOiCHJcFCP',
      crossorigin: 'anonymous',
    },
  ],
  themeConfig: {
    image: 'img/clarid-logo.png',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'ClarID-Tools',
      logo: {
        alt: 'ClarID-Tools',
        src: 'img/clarid-logo.png',
        srcDark: 'img/clarid-logo.png',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docsSidebar',
          position: 'left',
          label: 'Docs',
        },
        {
          to: '/usage/quickstart',
          label: 'Quickstart',
          position: 'left',
        },
        {
          to: '/usage/cli-reference',
          label: 'CLI',
          position: 'left',
        },
        {
          href: 'https://colab.research.google.com/drive/1smS42yzL7qYV1kCz34baTWLRr_AAap-r',
          label: 'Colab',
          position: 'left',
        },
        {
          href: 'https://github.com/CNAG-Biomedical-Informatics/clarid-tools',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {label: 'Introduction', to: '/'},
            {label: 'Quickstart', to: '/usage/quickstart'},
            {label: 'Codebook & Schema', to: '/technical-details/codebook-and-schema'},
          ],
        },
        {
          title: 'Project',
          items: [
            {label: 'Repository', href: 'https://github.com/CNAG-Biomedical-Informatics/clarid-tools'},
            {label: 'CPAN', href: 'https://metacpan.org/pod/ClarID::Tools'},
            {label: 'CNAG', href: 'https://www.cnag.eu'},
          ],
        },
      ],
      copyright: 'Copyright © 2025-2026 Manuel Rueda, CNAG.',
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
