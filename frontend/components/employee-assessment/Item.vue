<template>
  <NuxtLink
    :to="`/employee-assessments/${item.uid}`"
    class="flex items-center px-4 py-2 bg-base-100 rounded-xl border-2 border-primary/50 hover:border-primary cursor-pointer"
  >
    <div class="flex-1">
      <div class="text-xs font-bold text-base-content/50">{{ item.profile.name }}</div>
      <div class="text-lg font-black">{{ item.assessment.name }}</div>
    </div>
    <div v-if="item.completed_dt" class="flex justify-center items-center w-8 h-8 text-xl text-accent bg-accent/10 border-2 border-accent/50 rounded-md">
      <Icon name="ph:check-bold" />
    </div>
  </NuxtLink>
</template>

<script setup lang="ts">
defineProps<{
  item: EmployeeAssessment,
}>()
</script>

<style lang="pcss" scoped>

</style>
