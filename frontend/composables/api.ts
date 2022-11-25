export const useApi = async (url: string) => {
  const config = useRuntimeConfig()
  const { data } = await useFetch(config.apiUrl + url)
  return data
}
