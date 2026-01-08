'use client';

import { useEffect } from 'react';

export function SuppressWarnings() {
  useEffect(() => {
    // Store the original console.error
    const originalError = console.error.bind(console);

    // Override console.error to filter out the warning
    console.error = function (...args: unknown[]) {
      // Filter out Ed25519 and other crypto warnings
      const message = args[0];
      if (
        typeof message === 'string' &&
        (message.includes('Ed25519') ||
         message.includes('crypto') ||
         message.includes('experimental') ||
         message.includes('Web Crypto API'))
      ) {
        return;
      }
      originalError(...args);
    };

    // Cleanup function to restore original console.error
    return () => {
      console.error = originalError;
    };
  }, []);

  return null;
}