<template>
  <NuxtLayout name="page">
    <div class="navbar bg-base-200">
      <a
        class="btn btn-ghost normal-case text-xl"
        @click="router.back()"
      >
        <Icon name="ph:arrow-left-bold" class="mr-2" />Back
      </a>
    </div>
    <div class="hero">
      <div class="py-12 text-center hero-content">
        <div class="max-w-screen-md">
          <h1 class="mt-4 mb-8 text-5xl font-black">
            Assessent
          </h1>
          <p>
            of {{ }} for role {{ }}
          </p>
          <p>
            Please answer the following questions and click submit when done.
          </p>
        </div>
      </div>
    </div>
    <div class="flex justify-center bg-primary/20">
      <div class="w-full max-w-screen-md py-12">

      </div>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const route = useRoute()
const router = useRouter()

const uid = $computed(() => route.params.uid?.toString())
const employeeAssessment = useApi(`/assessments/employee-assessment/${uid}`)
</script>
