import { defineConfig } from 'vitest/config';

const src = new URL('./src', import.meta.url).pathname;

export default defineConfig({
  resolve: {
    alias: {
      '@': src,
      // The real package throws outside React Server Components.
      'server-only': new URL('./test/fakes/server-only.ts', import.meta.url).pathname,
    },
  },
  test: { include: ['test/**/*.test.ts'] },
});
