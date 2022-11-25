declare interface user {
  id: number,
  name: string,
}

declare interface Role {
  id: number,
  name: string,
}

declare interface Assessment {
  id: number,
  name: string,
}

declare interface EmployeeAssessment {
  id: number,
  profile: number,
  assessment: number,
}
