export default defineNuxtConfig({
  runtimeConfig: {
    public: {}
  },
  app: {
    head: {
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
  tailwindcss: {
    cssPath: '~/assets/css/tailwind.css',
  },
  colorMode: {
    classSuffix: '',
    dataValue: 'theme',
    preference: 'system',
  },
  typescript: {
    shim: false,
  },
})
