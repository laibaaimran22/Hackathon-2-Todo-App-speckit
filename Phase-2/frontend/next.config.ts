import type { NextConfig } from "next";

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
