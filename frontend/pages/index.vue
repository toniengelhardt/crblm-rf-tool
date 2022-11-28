<template>
  <NuxtLayout name="page">
    <div class="hero">
      <div class="py-12 text-center hero-content">
        <div class="max-w-screen-md">
          <p class="text-xl font-black text-base-content/50">crblm</p>
          <h1 class="mt-4 mb-8 text-6xl font-black">
            RF <span class="text-primary/50">/</span> Tool
          </h1>
          <p class="italic">
            You can define roles, questions, assessments, etc. in the
            <NuxtLink
              :to="`${config.backendUrl}/admin`"
              target="_blank"
              title="Backend"
              class="link font-bold"
            >backend</NuxtLink>.
          </p>
          <p class="mt-2 italic">
            Click on an assessment to open it <Icon name="ph:arrow-down-bold" class="text-primary" />
          </p>
        </div>
      </div>
    </div>
    <div class="flex justify-center p-4 md:py-12 bg-base-content">
      <div class="w-full max-w-screen-md">
        <EmployeeAssessmentList :items="employeeAssessments" />
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { Ref } from 'vue'

const config = useRuntimeConfig()
const employeeAssessments = await useApi('/assessments/employee-assessments') as Ref<EmployeeAssessment[]>
</script>
