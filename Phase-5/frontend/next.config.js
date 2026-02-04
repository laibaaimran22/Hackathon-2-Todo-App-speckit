/** @type {import('next').NextConfig} */
const nextConfig = {
  // Use webpack instead of Turbopack
  experimental: {
    appDir: true,
  },

  // Proxy API requests to the backend server
  async rewrites() {
    return [
      {
        source: '/api/auth/:path*',
        destination: 'http://localhost:8000/api/auth/:path*',
      },
      {
        source: '/api/tasks/:path*',
        destination: 'http://localhost:8000/api/tasks/:path*',
      },
      {
        source: '/api/debug/:path*',
        destination: 'http://localhost:8000/api/debug/:path*',
      },
      {
        source: '/mcp/:path*',
        destination: 'http://localhost:8000/mcp/:path*',
      },
    ];
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
        ],
      },
    ];
  },
};

module.exports = nextConfig;