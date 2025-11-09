/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://sumo-claude-code.onrender.com/api/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
