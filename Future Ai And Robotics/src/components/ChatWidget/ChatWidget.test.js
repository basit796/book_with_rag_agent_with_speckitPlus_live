import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatWidget from './ChatWidget';

// Mock framer-motion to avoid animation issues in tests
jest.mock('framer-motion', () => ({
  motion: {
    button: ({ children, onClick, ...props }) => (
      <button onClick={onClick} {...props}>{children}</button>
    ),
    div: ({ children, ...props }) => <div {...props}>{children}</div>,
  },
  AnimatePresence: ({ children }) => <>{children}</>,
}));

// Mock fetch
global.fetch = jest.fn();

describe('ChatWidget', () => {
  beforeEach(() => {
    // Clear localStorage
    localStorage.clear();
    // Clear fetch mock
    global.fetch.mockClear();
  });

  test('renders chat button', () => {
    render(<ChatWidget />);
    const button = screen.getByLabelText(/open chat/i);
    expect(button).toBeInTheDocument();
  });

  test('opens chat panel on button click', () => {
    render(<ChatWidget />);
    const button = screen.getByLabelText(/open chat/i);
    fireEvent.click(button);
    
    expect(screen.getByText('Book Assistant')).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/ask a question/i)).toBeInTheDocument();
  });

  test('closes chat panel on close button click', () => {
    render(<ChatWidget />);
    
    // Open chat
    const openButton = screen.getByLabelText(/open chat/i);
    fireEvent.click(openButton);
    
    // Close chat
    const closeButton = screen.getByLabelText(/close chat/i);
    fireEvent.click(closeButton);
    
    expect(screen.queryByText('Book Assistant')).not.toBeInTheDocument();
  });

  test('displays empty state message initially', () => {
    render(<ChatWidget />);
    
    // Open chat
    fireEvent.click(screen.getByLabelText(/open chat/i));
    
    expect(screen.getByText(/ask me anything about the book/i)).toBeInTheDocument();
  });

  test('submits question and displays response', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        answer: 'Test answer about physical AI',
        citations: [
          {
            module_title: 'Module 1',
            chapter_title: 'Introduction',
            file_path: 'docs/module-1/01-intro.md'
          }
        ],
        session_id: 'test-session'
      })
    });

    render(<ChatWidget />);
    
    // Open chat
    fireEvent.click(screen.getByLabelText(/open chat/i));
    
    // Type message (must be at least 10 characters)
    const input = screen.getByPlaceholderText(/ask a question/i);
    fireEvent.change(input, { target: { value: 'What is physical AI and robotics?' } });
    
    // Submit
    const sendButton = screen.getByText(/send/i);
    fireEvent.click(sendButton);
    
    // Wait for response
    await waitFor(() => {
      expect(screen.getByText('Test answer about physical AI')).toBeInTheDocument();
    });
    
    // Check citation is displayed
    expect(screen.getByText(/Module 1 → Introduction/i)).toBeInTheDocument();
  });

  test('displays error message on API failure', async () => {
    global.fetch.mockRejectedValueOnce(new Error('Network error'));

    render(<ChatWidget />);
    
    // Open chat
    fireEvent.click(screen.getByLabelText(/open chat/i));
    
    // Submit message
    const input = screen.getByPlaceholderText(/ask a question/i);
    fireEvent.change(input, { target: { value: 'What is physical AI?' } });
    fireEvent.click(screen.getByText(/send/i));
    
    // Wait for error message
    await waitFor(() => {
      expect(screen.getByText(/encountered an error/i)).toBeInTheDocument();
    });
  });

  test('validates minimum message length', () => {
    render(<ChatWidget />);
    
    // Open chat
    fireEvent.click(screen.getByLabelText(/open chat/i));
    
    // Try to send short message
    const input = screen.getByPlaceholderText(/ask a question/i);
    fireEvent.change(input, { target: { value: 'Hi' } });
    
    const sendButton = screen.getByText(/send/i);
    expect(sendButton).toBeDisabled();
  });

  test('generates and stores session ID', () => {
    render(<ChatWidget />);
    
    // Wait a bit for useEffect to run
    setTimeout(() => {
      const sessionId = localStorage.getItem('chat_session_id');
      expect(sessionId).toBeTruthy();
      expect(sessionId).toContain('session_');
    }, 100);
  });

  test('closes chat on Escape key', () => {
    render(<ChatWidget />);
    
    // Open chat
    fireEvent.click(screen.getByLabelText(/open chat/i));
    expect(screen.getByText('Book Assistant')).toBeInTheDocument();
    
    // Press Escape
    fireEvent.keyDown(document, { key: 'Escape' });
    
    expect(screen.queryByText('Book Assistant')).not.toBeInTheDocument();
  });
});
