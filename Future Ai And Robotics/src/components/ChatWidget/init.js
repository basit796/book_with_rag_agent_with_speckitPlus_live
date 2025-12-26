import React from 'react';
import { createRoot } from 'react-dom/client';
import ChatWidget from './ChatWidget';
import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';

// Only run in browser environment
if (ExecutionEnvironment.canUseDOM) {
  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initChatWidget);
  } else {
    initChatWidget();
  }
}

function initChatWidget() {
  // Check if widget is already initialized
  if (document.getElementById('chat-widget-root')) {
    return;
  }

  // Create container
  const container = document.createElement('div');
  container.id = 'chat-widget-root';
  document.body.appendChild(container);

  // Render widget
  const root = createRoot(container);
  root.render(<ChatWidget />);
}

export default function ChatWidgetInit() {
  return null; // This component doesn't render anything
}
