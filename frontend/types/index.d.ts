declare interface user {
  id: number,
  name: string,
}

declare interface Role {
  id: number,
  name: string,
}

declare interface Question {
  id: number,
  text: string,
  reference: string,
}

declare interface Assessment {
  id: number,
  name: string,
  questions: Question[],
}

declare interface EmployeeAssessment {
  id: number,
  uid: string,
  profile: number,
  assessment: Assessment,
  completed_dt: string,
}
