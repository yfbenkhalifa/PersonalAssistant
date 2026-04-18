import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  const isLibrary = mode === 'library'

  return {
    plugins: [react()],
    server: {
      port: 3000,
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
        },
        '/ws': {
          target: 'ws://localhost:8000',
          ws: true,
        },
      },
    },
    build: isLibrary
      ? {
          lib: {
            entry: './src/index.js',
            name: 'PersonalAssistantFrontend',
            fileName: (format) =>
              format === 'es'
                ? 'personal-assistant-frontend.js'
                : 'personal-assistant-frontend.umd.cjs',
            formats: ['es', 'umd'],
          },
          rollupOptions: {
            external: ['react', 'react-dom'],
            output: {
              globals: {
                react: 'React',
                'react-dom': 'ReactDOM',
              },
            },
          },
        }
      : undefined,
  }
})
