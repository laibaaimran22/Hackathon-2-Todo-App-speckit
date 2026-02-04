/** @type {import('next').NextConfig} */
const nextConfig = {
  // Proxy backend API requests in production
  async rewrites() {
    const apiBase = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000").replace(/\/$/, "");
    return [
      {
        source: '/api/tasks/:path*',
        destination: `${apiBase}/api/tasks/:path*`,
      },
      {
        source: '/api/debug/:path*',
        destination: `${apiBase}/api/debug/:path*`,
      },
      {
        source: '/mcp/:path*',
        destination: `${apiBase}/mcp/:path*`,
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
