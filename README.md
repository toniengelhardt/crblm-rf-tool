# Cerebellum RF Tool

[ monorepo ]

MVP based on Django + Postgres DB (backend), Vue/Nuxt, Vite, Tailwind, and Daisy UI (frontend).

### What can it do?

#### Backend

Default Django backend where you can manage all things, aka. define **Roles**, **Questions**, **Assessments**, etc. and generate `EmployeeAssessment` instances that can be interacted with in the frontend.

#### Frontend

For now there is a list with all the `EmployeeAssessments` generated in the backend and assessment pages with unique links where you can answer the queestions and submit them.
