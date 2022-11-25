<template>
  <div class="grid gap-8">
    <div
      v-for="(question, idx) in employeeAssessment.assessment.questions"
      :key="question.id"
    >
      <div class="ml-4 text-3xl font-black text-base-100">
        {{ idx + 1 }}.
      </div>
      <div
        class="mt-2 p-4 text-lg bg-base-100 rounded-lg shadow"
      >
        <div>
          {{ question.text }}
        </div>
        <div>
          <textarea
            class="textarea textarea-bordered w-full mt-4 px-3 text-lg rounded-md"
            placeholder="Your answer..."
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  employeeAssessment: EmployeeAssessment,
}>()
</script>

<style lang="pcss" scoped>

</style>
