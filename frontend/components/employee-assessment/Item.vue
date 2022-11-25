<template>
  <NuxtLink
    :to="`/ea/${item.id}`"
    target="_blank"
    class="flex items-center px-4 py-3 bg-base-100 rounded-lg hover:bg-base-300 cursor-pointer"
  >
    <div class="flex-1">
      <div class="text-sm font-bold text-base-content/50">{{ item.profile.name }}</div>
      <div class="text-lg font-black">{{ item.assessment.name }}</div>
      <div class="text-xs italic">{{ item.assessment.questions.length }} question{{ item.assessment.questions.length !== 1 ? 's' : '' }}</div>
    </div>
    <div
      v-if="item.completed_dt"
      class="flex justify-center items-center w-8 h-8 mr-4 text-2xl border-2 border-base-content rounded-md"
    >
      <Icon name="ph:check-bold" />
    </div>
  </NuxtLink>
</template>

<script setup lang="ts">
const props = defineProps<{
  item: EmployeeAssessment,
}>()
</script>

<style lang="pcss" scoped>

</style>
