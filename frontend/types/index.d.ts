declare interface user {
  id: string,
  name: string,
}

declare interface Role {
  id: string,
  name: string,
}

declare interface Question {
  id: string,
  text: string,
  reference: string,
}

declare interface Assessment {
  id: string,
  name: string,
  role: Role,
  questions: Question[],
}

declare interface EmployeeAssessment {
  id: string,
  profile: Profile,
  assessment: Assessment,
  completed_dt: string,
}
