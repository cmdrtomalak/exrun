import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    include: ['exercises/**/tests/*.{test,spec}.ts'],
  },
});
