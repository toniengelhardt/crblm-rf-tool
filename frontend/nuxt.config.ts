export default defineNuxtConfig({
  telemetry: false,
  runtimeConfig: {
    public: {
      backendUrl: process.env.BACKEND_URL,
      apiUrl: process.env.API_URL,
    }
  },
  app: {
    head: {
      htmlAttrs: {
        lang: 'en',
        translate: 'no', // Avoid translation.
      },
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1.0',
    },
  },
  modules: [
    '@nuxtjs/color-mode',
    '@nuxtjs/tailwindcss',
    '@vueuse/nuxt',
    'nuxt-icon',
  ],
  vite: {
    vue: {
      reactivityTransform: true,
    },
  },
  // tailwindcss: {
  //   cssPath: '~/assets/css/tailwind.css',
  // },
  colorMode: {
    classSuffix: '',
    dataValue: 'theme',
    preference: 'system',
  },
  typescript: {
    shim: false,
  },
})
