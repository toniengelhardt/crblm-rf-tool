<template>
  <div class="bg-base-100 rounded-lg overflow-hidden">
    <NuxtLink
      :to="`/ea/${item.id}`"
      target="_blank"
      class="flex items-center px-4 py-3 hover:bg-base-200 cursor-pointer"
    >
      <div class="flex-1">
        <div class="text-sm font-bold text-base-content/50">
          {{ item.profile.name }}
        </div>
        <div class="text-lg font-black">
          {{ item.assessment.name }}
        </div>
        <div class="text-xs italic">
          {{ answerCount }} / {{ questionCount }}
          question{{ questionCount !== 1 ? 's' : '' }} answered
        </div>
      </div>
      <div
        v-if="item.completed_dt"
        class="flex justify-center items-center w-8 h-8 mr-4 text-2xl border-2 border-lime-500 rounded-md"
      >
        <Icon name="ph:check-bold" class="text-lime-500" />
      </div>
    </NuxtLink>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  item: EmployeeAssessment
}>()

const questionCount = $computed(() => props.item.answers.length)
const answerCount = $computed(() => props.item.answers.filter(answer => answer.text !== '').length)
</script>
