import { Ref } from 'vue'

export const useUpdateEmployeeAssessment = async (
  employeeAssessment: Ref<EmployeeAssessment>,
  data: Partial<EmployeeAssessment>,
) => {
  const _employeeAssessment = await useApi(`/assessments/employee-assessments/${employeeAssessment.value.id}/`, {
    method: 'PATCH',
    body: JSON.stringify(data)
  }) as Ref<EmployeeAssessment>
  employeeAssessment.value = _employeeAssessment.value
}

export const useUpdateAnswer = async (
  answer: Ref<Answer>,
  data: Partial<Answer>,
) => {
  const _answer = await useApi(`/assessments/answers/${answer.value.id}/`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  }) as Ref<Answer>
  answer.value = _answer.value
}
