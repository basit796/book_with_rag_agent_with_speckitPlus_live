// @ts-check

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.

 @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  tutorialSidebar: [
    'intro',
    'how-to-use',
    {
      type: 'category',
      label: 'Module 1: Physical AI Foundations',
      collapsed: false,
      items: [
        'module-1-physical-ai/what-is-physical-ai',
        'module-1-physical-ai/physical-constraints',
        'module-1-physical-ai/robot-architecture',
        'module-1-physical-ai/why-humanoids',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: ROS2 Middleware',
      collapsed: false,
      items: [
        'module-2-ros2/why-middleware',
        'module-2-ros2/architecture',
        'module-2-ros2/communication-patterns',
        'module-2-ros2/python-integration',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: Simulation Foundations',
      collapsed: false,
      items: [
        'module-3-simulation/why-simulation-first',
        'module-3-simulation/physics-digital-twins',
        'module-3-simulation/simulated-sensors',
        'module-3-simulation/tools-landscape',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: NVIDIA Isaac Platform',
      collapsed: false,
      items: [
        'module-4-isaac/why-better-simulation',
        'module-4-isaac/isaac-sim-overview',
        'module-4-isaac/isaac-ros-pipelines',
        'module-4-isaac/mapping-navigation',
      ],
    },
  ],
};

export default sidebars;
