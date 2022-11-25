<template>
  <NuxtLayout name="page">
    <div class="hero">
      <div class="py-12 text-center hero-content">
        <div class="max-w-screen-md">
          <h1 class="mb-2 text-5xl font-black">
            Assessment
          </h1>
          <p class="text-2xl font-bold mb-8 text-base-content/50">
            {{ employeeAssessment?.profile.name || '...' }} <span class="text-primary/50">/</span>
            {{ employeeAssessment?.assessment.role.name || '...' }}
          </p>
          <p class="mt-2">
            Please answer the following questions and click submit when done.
          </p>
          <p>
            Answers will be saved.
          </p>
        </div>
      </div>
    </div>
    <div class="flex justify-center p-4 md:py-12 from-primary to-accent bg-gradient-to-br">
      <div class="w-full max-w-screen-md">
        <EmployeeAssessmentQuestionaire :employeeAssessment="employeeAssessment" />
        <p class="mt-4 md:mt-8 text-center text-xl font-bold text-base-100">Great, all done!</p>
      </div>
    </div>
    <div class="flex justify-center p-4 md:py-12">
      <div>
        <button
          v-if="!employeeAssessment.completed_dt"
          class="btn btn-primary"
          @click="submitAssessment()"
        >Submit assessment</button>
        <p v-else>
          Assessment was submitted, but you can still edit it.
        </p>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { Ref } from 'vue'

const route = useRoute()

let employeeAssessment = await useApi(`/assessments/employee-assessments/${route.params.id.toString()}`) as Ref<EmployeeAssessment>

async function submitAssessment() {
  employeeAssessment = await useApi(`/assessments/employee-assessments/${employeeAssessment.value.id}/`, {
    method: 'PATCH',
    body: JSON.stringify({
      completed_dt: new Date().toISOString(),
    })
  }) as Ref<EmployeeAssessment>
}
</script>
