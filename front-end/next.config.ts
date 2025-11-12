/** @type {import('next').NextConfig} */
const nextConfig = {
  // Export static site to ./out
  output: 'export',
  experimental: {
    // These are not officially supported but since the backend is just a django dev server the
    // load from multiple threads is too much to handle during builds. More context below:
    // https://docs.uniform.dev/sitecore/deploy/how-tos/how-to-control-nextjs-threads/
    // https://github.com/vercel/next.js/issues/36174#issuecomment-1100104594
    workerThreads: false,
    cpus: 1
  },
};

export default nextConfig;
