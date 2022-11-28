<template>
  <div v-if="employeeAssessment" class="grid gap-8">
    <div
      v-for="(answer, idx) in employeeAssessment.answers"
      :key="answer.id"
    >
      <div class="ml-6 text-3xl font-black text-primary">
        {{ idx + 1 }}.
      </div>
      <div
        class="mt-2 px-4 py-3 text-lg bg-base-100 rounded-lg shadow"
      >
        <div>
          {{ answer.question.text }}
        </div>
        <div class="mt-3">
          <textarea
            :value="answer.text || ''"
            class="textarea textarea-bordered w-full px-3 text-lg bg-base-300 border-0 rounded-md"
            placeholder="Your answer..."
            @keydown.enter.prevent
            @keyup.enter="$event.target?.blur()"
            @change="updateAnswer(ref(answer), $event)"
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

async function updateAnswer(answer: Ref<Answer>, event: any) {
  await useUpdateAnswer(answer, { text: event.target.value })
}
</script>

<style lang="pcss" scoped>

</style>
