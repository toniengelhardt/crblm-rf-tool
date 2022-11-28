<template>
  <div class="flex flex-col min-h-screen">
    <div class="flex-1">
      <slot />
    </div>
    <footer class="p-4 bg-base-200">
      <div class="flex justify-center mt-2 mb-4">
        <ClientOnly>
          <select v-model="colorMode.preference" class="select select-bordered select-sm w-60">
            <option disabled selected>Theme</option>
            <option v-for="theme of themes" :key="theme">{{ theme }}</option>
          </select>
        </ClientOnly>
      </div>
      <div class="w-full text-center text-sm">
        <p>
          &copy; 2022 Toni Engelhardt
        </p>
        <p class="mt-1">
          Made with <b>Django</b>, <b>Nuxt</b>, <b>Vite</b>, <b>Tailwind</b>, and <b>Daisy UI</b>.
        </p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
const colorMode = useColorMode()

const themes = [
  'light',
  'dark',
  'cupcake',
  'bumblebee',
  'emerald',
  'corporate',
  'synthwave',
  'retro',
  'cyberpunk',
  'valentine',
  'halloween',
  'garden',
  'forest',
  'aqua',
  'lofi',
  'pastel',
  'fantasy',
  'wireframe',
  'black',
  'luxury',
  'dracula',
  'cmyk',
  'autumn',
  'business',
  'acid',
  'lemonade',
  'night',
  'coffee',
  'winter',
]
</script>
