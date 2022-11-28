<template>
  <div class="grid gap-4 md:gap-8">
    <div
      v-for="(answer, idx) in employeeAssessment.answers"
      :key="answer.id"
    >
      <div class="ml-4 md:ml-6 text-xl md:text-3xl font-black text-accent">
        {{ idx + 1 }}.
      </div>
      <div class="mt-2 px-4 py-3 text-lg bg-base-100 border-0 border-accent rounded-lg shadow">
        <div>
          {{ answer.question.text }}
        </div>
        <div class="mt-3">
          <textarea
            :value="answer.text || ''"
            class="textarea textarea-bordered w-full px-3 text-lg bg-base-200 border border-base-300 rounded-md"
            placeholder="Your answer..."
            @keydown.enter.prevent
            @keyup.enter="($event.target as HTMLInputElement)?.blur()"
            @change="updateAnswer(answer, $event)"
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

async function updateAnswer(answer: Answer, event: any) {
  await useUpdateAnswer(ref(answer), { text: event.target.value })
}
</script>
