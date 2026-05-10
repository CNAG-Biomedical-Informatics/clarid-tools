import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docsSidebar: [
    {
      type: 'doc',
      id: 'overview',
      label: 'Overview',
    },
    {
      type: 'category',
      label: 'Download & Installation',
      items: [
        {type: 'doc', id: 'download-and-installation/non-containerized', label: 'Non-containerized'},
        {type: 'doc', id: 'download-and-installation/docker-based', label: 'Docker-based'},
      ],
    },
    {
      type: 'category',
      label: 'Getting Started',
      items: [
        {type: 'doc', id: 'usage/quickstart', label: 'Quickstart'},
        {type: 'doc', id: 'usage/cli-reference', label: 'CLI Reference'},
      ],
    },
    {
      type: 'category',
      label: 'Use Cases',
      items: [
        {type: 'doc', id: 'use-cases/subject', label: 'Subject'},
        {type: 'doc', id: 'use-cases/biosample', label: 'Biosample'},
      ],
    },
    {
      type: 'category',
      label: 'Technical Details',
      items: [
        {type: 'doc', id: 'technical-details/implementation', label: 'Implementation'},
        {type: 'doc', id: 'technical-details/specification', label: 'Specification'},
        {type: 'doc', id: 'technical-details/codebook-and-schema', label: 'Codebook & Schema'},
        {type: 'doc', id: 'technical-details/pre-processing-script', label: 'Pre-processing Script'},
        {type: 'doc', id: 'technical-details/use-from-r', label: 'Use from R'},
      ],
    },
    {
      type: 'category',
      label: 'Help',
      items: [
        {type: 'doc', id: 'help/faq', label: 'FAQs'},
        {
          type: 'link',
          href: 'https://colab.research.google.com/drive/1smS42yzL7qYV1kCz34baTWLRr_AAap-r',
          label: 'Google Colab',
        },
      ],
    },
    {
      type: 'category',
      label: 'About',
      items: [
        {type: 'doc', id: 'about/about', label: 'About'},
        {type: 'doc', id: 'about/citation', label: 'Citation'},
      ],
    },
  ],
};

export default sidebars;
