<template>
  <NuxtLayout name="page">
    <div class="hero">
      <div class="py-8 md:py-12 text-center hero-content">
        <div class="max-w-screen-md text-sm md:text-md">
          <h1 class="mb-2 text-4xl md:text-5xl font-black">
            Assessment
          </h1>
          <p class="text-xl md:text-2xl font-bold mb-4 md:mb-8 text-base-content/50">
            {{ employeeAssessment?.profile.name || '...' }} <span class="text-primary/50">/</span>
            {{ employeeAssessment?.assessment.role.name || '...' }}
          </p>
          <p class="mt-2">
            Please answer the following questions and click submit when done.
          </p>
        </div>
      </div>
    </div>
    <div class="flex justify-center p-4 md:py-12 bg-base-content">
      <div class="w-full max-w-screen-md">
        <EmployeeAssessmentQuestionaire :employeeAssessment="employeeAssessment" />
        <p class="mt-4 md:mt-8 text-center text-xl font-bold text-base-100">Great, all done!</p>
      </div>
    </div>
    <div class="flex justify-center p-4 md:py-12">
      <div class="text-center">
        <button
          v-if="!employeeAssessment.completed_dt"
          class="btn btn-lg btn-primary text-base-100"
          @click="submitAssessment()"
        >Submit assessment<Icon name="ph:paper-plane-tilt-duotone" class="ml-2" /></button>
        <div v-else class="flex flex-col items-center">
          <div class="flex justify-center items-center w-12 h-12 mb-4 bg-green-200 rounded-full">
            <Icon name="ph:check-bold" class="text-green-500" size="1.6rem" />
          </div>
          <p>Assessment was submitted, but you can still edit it.</p>
          <p><a class="link" @click="withdrawAssessment()">Withdraw</a></p>
        </div>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { Ref } from 'vue'
import { useUpdateEmployeeAssessment } from '~~/composables/assessment'

const route = useRoute()

const employeeAssessment = await useApi(`/assessments/employee-assessments/${route.params.id.toString()}`) as Ref<EmployeeAssessment>

async function submitAssessment() {
  await useUpdateEmployeeAssessment(employeeAssessment, {
    completed_dt: new Date().toISOString(),
  })
}
async function withdrawAssessment() {
  useUpdateEmployeeAssessment(employeeAssessment, {
    completed_dt: null,
  })
}
</script>
