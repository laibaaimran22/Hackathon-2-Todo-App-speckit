import type { NextConfig } from "next";

// Suppress Node.js experimental warnings (like Ed25519 from better-auth)
const originalEmit = process.emit;
// @ts-expect-error - process.emit types don't match but this works
process.emit = function (name, data, ...args) {
  if (
    name === 'warning' &&
    typeof data === 'object' &&
    data.name === 'ExperimentalWarning'
  ) {
    return false;
  }
  // @ts-expect-error - TypeScript doesn't like this but it's necessary
  return originalEmit.apply(process, arguments);
};

const nextConfig: NextConfig = {
  // Suppress experimental feature warnings
  experimental: {
    serverMinification: true,
  },

  // Suppress console warnings in development
  webpack: (config) => {
    return config;
  },
};

export default nextConfig;
