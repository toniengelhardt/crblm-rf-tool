<template>
  <div class="drawer drawer-mobile">
    <input id="drawer" type="checkbox" class="drawer-toggle">
    <div class="drawer-content">
      <slot />
    </div>
    <div class="drawer-side">
      <label for="drawer" class="drawer-overlay"></label>
      <aside class="bg-base-200 w-80">
        <div class="z-20 bg-base-200 backdrop-blur sticky top-0 items-center gap-2 p-2 hidden lg:flex">
          <a href="/" aria-current="page" aria-label="Homepage" class="flex-0 btn btn-ghost px-2">
            <div class="font-title text-primary inline-flex text-lg transition-all duration-200 md:text-3xl">
              MVP
            </div>
          </a>
        </div>
        <div class="p-4">
          Description here...
        </div>
      </aside>
    </div>
  </div>
</template>
