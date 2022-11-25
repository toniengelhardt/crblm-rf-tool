<template>
  <div class="grid gap-4">
    <EmployeeAssessmentItem
      v-for="item in items"
      :item="item"
    />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  items: EmployeeAssessment[],
}>()
</script>
