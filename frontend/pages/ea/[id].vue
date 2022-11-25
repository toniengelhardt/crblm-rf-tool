<template>
  <NuxtLayout name="page">
    <!-- <div class="navbar bg-base-200">
      <a
        class="btn btn-ghost normal-case text-xl"
        @click="router.back()"
      >
        <Icon name="ph:arrow-left-bold" class="mr-2" />Back
      </a>
    </div> -->
    <div class="hero">
      <div class="py-12 text-center hero-content">
        <div class="max-w-screen-md">
          <h1 class="mt-4 mb-8 text-5xl font-black">
            Assessent
          </h1>
          <p>
            <strong>{{ employeeAssessment?.profile.name || '...' }}</strong> for <strong>{{ employeeAssessment?.assessment.role.name || '...' }}</strong> role.
          </p>
          <p class="mt-2">
            Please answer the following questions and click submit when done.
          </p>
        </div>
      </div>
    </div>
    <div class="flex justify-center bg-primary/20">
      Hello
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { Ref } from 'vue'

const route = useRoute()
const router = useRouter()

const employeeAssessment = await useApi(`/assessments/employee-assessments/${route.params.id.toString()}`) as Ref<EmployeeAssessment>
</script>
