import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Suppress experimental feature warnings
  experimental: {
    serverMinification: true,
    // Handle route groups properly during build
    typedRoutes: false, // Disable typed routes which can cause issues with route groups
  },

  // Suppress console warnings in development
  webpack: (config) => {
    return config;
  },
};

export default nextConfig;
