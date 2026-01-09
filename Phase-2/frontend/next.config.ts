import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Updated for Next.js 16 compatibility
  typedRoutes: false, // Moved from experimental

  // Enable Turbopack compatibility
  webpack: (config, { dev, isServer }) => {
    // Return config as-is, but make it compatible with Turbopack
    return config;
  },

  // Empty turbopack config to satisfy the requirement
  turbopack: {},
};

export default nextConfig;
