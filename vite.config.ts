import { defineConfig } from 'vitest/config'

// https://vitejs.dev/config/
export default defineConfig({
  base: '',
  define: {
    'import.meta.vitest': 'undefined',
  },
  resolve: {
    alias: [{ find: '@', replacement: '/pbhhg_js' }],
  },
  test: {
    includeSource: ['pbhhg_js/**/*.{js,ts}'],
  },
})
