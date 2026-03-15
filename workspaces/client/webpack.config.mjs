import path from 'node:path';

import { EsbuildPlugin } from 'esbuild-loader';
import webpack from 'webpack';
import { BundleAnalyzerPlugin } from 'webpack-bundle-analyzer';

const useBundleAnalyzer = false;

/** @type {import('webpack').Configuration} */
const config = {
  cache: {
    cacheDirectory: path.resolve(import.meta.dirname, '.webpack_cache'),
    type: 'filesystem',
  },
  // devtool: 'source-map',
  entry: './src/main.tsx',
  mode: 'production',
  module: {
    rules: [
      {
        exclude: [/node_modules\/video\.js/, /node_modules\/@videojs/],
        // exclude: [/node_modules\/*\/.js/],
        loader: 'esbuild-loader',
        options: {
          target: 'chrome140',
          tsconfig: 'tsconfig.json',
        },
        resolve: {
          fullySpecified: false,
        },
        test: /\.[jt]sx?$/,
      },
      {
        test: /\.png$/,
        type: 'asset/inline',
      },
      {
        resourceQuery: /raw/,
        type: 'asset/source',
      },
    ],
  },
  output: {
    chunkFilename: 'chunk-[contenthash].js',
    filename: 'main.js',
    path: path.resolve(import.meta.dirname, './dist'),
    publicPath: 'auto',
  },
  plugins: [new webpack.EnvironmentPlugin({ API_BASE_URL: '/api', NODE_ENV: '' })],
  resolve: {
    extensions: ['.js', '.cjs', '.mjs', '.ts', '.cts', '.mts', '.tsx', '.jsx'],
  },
};

if (useBundleAnalyzer && BundleAnalyzerPlugin) {
  // eslint-disable-next-line @typescript-eslint/no-unsafe-argument, @typescript-eslint/no-unsafe-call
  config.plugins?.push(new BundleAnalyzerPlugin());
} else {
  config.optimization = {
    minimizer: [
      new EsbuildPlugin({
        css: true,
        target: 'chrome140',
      }),
    ],
  };
}

export default config;
