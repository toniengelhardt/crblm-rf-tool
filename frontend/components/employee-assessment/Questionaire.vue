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
            @change="saveAnswer($event)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Ref } from 'vue';

defineProps<{
  employeeAssessment: EmployeeAssessment,
}>()

async function saveAnswer(event: any) {
  answer = await useApi(`/assessments/answers/${employeeAssessment.value.id}/`, {
    method: 'PATCH',
    body: JSON.stringify({
      text: event.target.value,
    })
  }) as Ref<Answer>
}
</script>

<style lang="pcss" scoped>

</style>
