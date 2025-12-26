import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/book_with_rag_agent_with_speckitPlus_live/blog',
    component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/blog', '579'),
    exact: true
  },
  {
    path: '/book_with_rag_agent_with_speckitPlus_live/blog/archive',
    component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/blog/archive', 'dc1'),
    exact: true
  },
  {
    path: '/book_with_rag_agent_with_speckitPlus_live/blog/authors',
    component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/blog/authors', '097'),
    exact: true
  },
  {
    path: '/book_with_rag_agent_with_speckitPlus_live/blog/authors/all-sebastien-lorber-articles',
    component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/blog/authors/all-sebastien-lorber-articles', '05b'),
    exact: true
  },
  {
    path: '/book_with_rag_agent_with_speckitPlus_live/blog/authors/yangshun',
    component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/blog/authors/yangshun', 'ee5'),
    exact: true
  },
  {
    path: '/book_with_rag_agent_with_speckitPlus_live/blog/first-blog-post',
    component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/blog/first-blog-post', 'a0a'),
    exact: true
  },
  {
    path: '/book_with_rag_agent_with_speckitPlus_live/blog/long-blog-post',
    component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/blog/long-blog-post', '3d6'),
    exact: true
  },
  {
    path: '/book_with_rag_agent_with_speckitPlus_live/blog/mdx-blog-post',
    component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/blog/mdx-blog-post', 'd6a'),
    exact: true
  },
  {
    path: '/book_with_rag_agent_with_speckitPlus_live/blog/tags',
    component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/blog/tags', '535'),
    exact: true
  },
  {
    path: '/book_with_rag_agent_with_speckitPlus_live/blog/tags/docusaurus',
    component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/blog/tags/docusaurus', 'fd4'),
    exact: true
  },
  {
    path: '/book_with_rag_agent_with_speckitPlus_live/blog/tags/facebook',
    component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/blog/tags/facebook', 'bae'),
    exact: true
  },
  {
    path: '/book_with_rag_agent_with_speckitPlus_live/blog/tags/hello',
    component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/blog/tags/hello', 'cd3'),
    exact: true
  },
  {
    path: '/book_with_rag_agent_with_speckitPlus_live/blog/tags/hola',
    component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/blog/tags/hola', '7ab'),
    exact: true
  },
  {
    path: '/book_with_rag_agent_with_speckitPlus_live/blog/welcome',
    component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/blog/welcome', '346'),
    exact: true
  },
  {
    path: '/book_with_rag_agent_with_speckitPlus_live/markdown-page',
    component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/markdown-page', '3a4'),
    exact: true
  },
  {
    path: '/book_with_rag_agent_with_speckitPlus_live/docs',
    component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/docs', '37a'),
    routes: [
      {
        path: '/book_with_rag_agent_with_speckitPlus_live/docs',
        component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/docs', 'e52'),
        routes: [
          {
            path: '/book_with_rag_agent_with_speckitPlus_live/docs',
            component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/docs', '10f'),
            routes: [
              {
                path: '/book_with_rag_agent_with_speckitPlus_live/docs/how-to-use',
                component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/docs/how-to-use', '9f0'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_with_rag_agent_with_speckitPlus_live/docs/intro',
                component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/docs/intro', 'b00'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_with_rag_agent_with_speckitPlus_live/docs/module-1-physical-ai/physical-constraints',
                component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/docs/module-1-physical-ai/physical-constraints', '811'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_with_rag_agent_with_speckitPlus_live/docs/module-1-physical-ai/robot-architecture',
                component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/docs/module-1-physical-ai/robot-architecture', 'ba0'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_with_rag_agent_with_speckitPlus_live/docs/module-1-physical-ai/what-is-physical-ai',
                component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/docs/module-1-physical-ai/what-is-physical-ai', 'ee5'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_with_rag_agent_with_speckitPlus_live/docs/module-1-physical-ai/why-humanoids',
                component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/docs/module-1-physical-ai/why-humanoids', '44e'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_with_rag_agent_with_speckitPlus_live/docs/module-2-ros2/architecture',
                component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/docs/module-2-ros2/architecture', '3af'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_with_rag_agent_with_speckitPlus_live/docs/module-2-ros2/communication-patterns',
                component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/docs/module-2-ros2/communication-patterns', 'd63'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_with_rag_agent_with_speckitPlus_live/docs/module-2-ros2/python-integration',
                component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/docs/module-2-ros2/python-integration', 'acb'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_with_rag_agent_with_speckitPlus_live/docs/module-2-ros2/why-middleware',
                component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/docs/module-2-ros2/why-middleware', '14b'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_with_rag_agent_with_speckitPlus_live/docs/module-3-simulation/physics-digital-twins',
                component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/docs/module-3-simulation/physics-digital-twins', '5dd'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_with_rag_agent_with_speckitPlus_live/docs/module-3-simulation/simulated-sensors',
                component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/docs/module-3-simulation/simulated-sensors', '067'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_with_rag_agent_with_speckitPlus_live/docs/module-3-simulation/tools-landscape',
                component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/docs/module-3-simulation/tools-landscape', '667'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_with_rag_agent_with_speckitPlus_live/docs/module-3-simulation/why-simulation-first',
                component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/docs/module-3-simulation/why-simulation-first', '8f5'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_with_rag_agent_with_speckitPlus_live/docs/module-4-isaac/isaac-ros-pipelines',
                component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/docs/module-4-isaac/isaac-ros-pipelines', 'db6'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_with_rag_agent_with_speckitPlus_live/docs/module-4-isaac/isaac-sim-overview',
                component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/docs/module-4-isaac/isaac-sim-overview', '6de'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_with_rag_agent_with_speckitPlus_live/docs/module-4-isaac/mapping-navigation',
                component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/docs/module-4-isaac/mapping-navigation', 'fd8'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_with_rag_agent_with_speckitPlus_live/docs/module-4-isaac/why-better-simulation',
                component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/docs/module-4-isaac/why-better-simulation', '5d8'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/book_with_rag_agent_with_speckitPlus_live/',
    component: ComponentCreator('/book_with_rag_agent_with_speckitPlus_live/', '31f'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
