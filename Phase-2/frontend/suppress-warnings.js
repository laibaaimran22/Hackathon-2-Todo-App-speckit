// Suppress experimental warnings
process.removeAllListeners('warning');
process.on('warning', (warning) => {
  if (warning.name === 'ExperimentalWarning') {
    return; // Suppress experimental warnings
  }
  console.warn(warning);
});

// Start Next.js
require('next/dist/bin/next');
