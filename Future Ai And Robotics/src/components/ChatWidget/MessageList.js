import React, { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import styles from './MessageList.module.css';

export default function MessageList({ messages, isLoading }) {
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div className={styles.messageList}>
      {messages.length === 0 && !isLoading && (
        <div className={styles.emptyState}>
          <p className={styles.emptyIcon}>📚</p>
          <p className={styles.emptyText}>
            Ask me anything about the book!
          </p>
          <p className={styles.emptySubtext}>
            I can help you find information across all chapters.
          </p>
        </div>
      )}

      {messages.map((msg, index) => (
        <motion.div
          key={index}
          className={`${styles.message} ${styles[msg.sender]} ${msg.isError ? styles.error : ''}`}
          initial={{ opacity: 0, x: msg.sender === 'user' ? 20 : -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3, ease: "easeOut" }}
        >
          <div className={styles.messageContent}>
            <p className={styles.messageText}>{msg.text}</p>
            {msg.citations && msg.citations.length > 0 && (
              <div className={styles.citations}>
                <strong className={styles.citationsLabel}>Sources:</strong>
                <div className={styles.citationsList}>
                  {msg.citations.map((cite, i) => {
                    // Handle both old and new citation formats
                    const chapter = cite.chapter || cite.chapter_title || 'Unknown Chapter';
                    const module = cite.module || cite.module_title || '';
                    
                    // Extract link from chapter or file_path
                    let link = '#';
                    if (cite.file_path) {
                      link = `/${cite.file_path.replace('docs/', '').replace('.md', '')}`;
                    } else if (cite.chapter) {
                      // Try to construct link from chapter title
                      const chapterMatch = cite.chapter.match(/Chapter \d+: (.+)/);
                      if (chapterMatch) {
                        link = '#'; // Keep as placeholder
                      }
                    }
                    
                    return (
                      <span
                        key={i}
                        className={styles.citationBadge}
                        title={`${module} - ${chapter}`}
                      >
                        {module && `${module} → `}{chapter}
                      </span>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
          <span className={styles.timestamp}>
            {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
        </motion.div>
      ))}

      {isLoading && (
        <motion.div
          className={`${styles.message} ${styles.bot}`}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3 }}
        >
          <div className={styles.typingIndicator}>
            <span></span>
            <span></span>
            <span></span>
          </div>
        </motion.div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
}
