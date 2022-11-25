export const useApi = async (url: string, options?: any) => {
  const config = useRuntimeConfig()
  const { data } = await useFetch(config.apiUrl + url, options)
  return data
}
