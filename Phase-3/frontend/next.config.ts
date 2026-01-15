import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Updated for Next.js 16 compatibility
  typedRoutes: false, // Moved from experimental

  // Proxy API requests to the backend server
  async rewrites() {
    return [
      {
        source: '/mcp/:path*',
        destination: 'http://localhost:8000/mcp/:path*',
      },
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ]
  },

  // Allow external API requests
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET, POST, PUT, DELETE, OPTIONS' },
          { key: 'Access-Control-Allow-Headers', value: 'Content-Type, Authorization' },
        ]
      }
    ]
  },

  // Enable Turbopack compatibility
  webpack: (config, { dev, isServer }) => {
    // Return config as-is, but make it compatible with Turbopack
    return config;
  },

  // Empty turbopack config to satisfy the requirement
  turbopack: {},
};

export default nextConfig;
