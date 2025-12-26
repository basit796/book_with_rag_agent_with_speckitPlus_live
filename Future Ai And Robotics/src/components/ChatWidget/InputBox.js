import React, { useState } from 'react';
import styles from './InputBox.module.css';

export default function InputBox({ onSend, disabled }) {
  const [input, setInput] = useState('');
  const [charCount, setCharCount] = useState(0);
  
  const MIN_CHARS = 10;
  const MAX_CHARS = 500;

  const handleChange = (e) => {
    const text = e.target.value;
    if (text.length <= MAX_CHARS) {
      setInput(text);
      setCharCount(text.length);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmed = input.trim();
    
    if (trimmed.length >= MIN_CHARS && trimmed.length <= MAX_CHARS && !disabled) {
      onSend(trimmed);
      setInput('');
      setCharCount(0);
    }
  };

  const handleKeyDown = (e) => {
    // Submit on Enter (not Shift+Enter)
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const isValid = input.trim().length >= MIN_CHARS;
  const isOverLimit = charCount > MAX_CHARS;

  return (
    <form className={styles.inputBox} onSubmit={handleSubmit}>
      <div className={styles.inputWrapper}>
        <textarea
          id="chat-input"
          className={styles.input}
          value={input}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about the book..."
          disabled={disabled}
          rows={3}
          aria-label="Chat input"
          aria-describedby="char-counter"
        />
        <div className={styles.inputFooter}>
          <span
            id="char-counter"
            className={`${styles.charCounter} ${isOverLimit ? styles.overLimit : ''} ${charCount < MIN_CHARS ? styles.underLimit : ''}`}
          >
            {charCount}/{MAX_CHARS} {charCount < MIN_CHARS && `(min ${MIN_CHARS})`}
          </span>
          <button
            type="submit"
            className={styles.sendButton}
            disabled={disabled || !isValid}
            aria-label="Send message"
          >
            {disabled ? '...' : 'Send'}
          </button>
        </div>
      </div>
      {charCount > 0 && charCount < MIN_CHARS && (
        <p className={styles.hint}>Please enter at least {MIN_CHARS} characters</p>
      )}
    </form>
  );
}
