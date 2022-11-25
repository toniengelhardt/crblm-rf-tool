<template>
  <NuxtLayout name="page">
    <div class="hero">
      <div class="py-12 text-center hero-content">
        <div class="max-w-md">
          <p class="text-xl font-black text-base-content/50">crblm</p>
          <h1 class="mt-4 mb-8 text-6xl font-black">
            RF <span class="text-primary/50">/</span> Tool
          </h1>
          <p class="italic">
            You can define questions and assessments in the
            <NuxtLink to="/admin" class="link font-bold">backend</NuxtLink>.
          </p>
          <p class="mt-2 italic">
            Click on an assessment to start it <Icon name="ph:arrow-down-bold" class="text-primary" />
          </p>
        </div>
      </div>
    </div>
    <div class="flex justify-center bg-primary/20 p-4">
      <div class="w-full max-w-screen-md md:py-8">
        <EmployeeAssessmentList :items="employeeAssessments" />
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { Ref } from 'vue'

const roles = await useApi('/assessents/roles') as Ref<Role[]>
const employeeAssessments = await useApi('/assessments/employee-assessments') as Ref<EmployeeAssessment[]>

// const items = $computed(() => {
//   const dict: { [roleId: number]: { role: Role, assessments: Assessment[] } } = {}
//   roles.value.forEach(role => dict[role.id] = { role, assessments: [] })
//   assessments.value.forEach(assessment => dict[assessment.role])
// })
</script>
