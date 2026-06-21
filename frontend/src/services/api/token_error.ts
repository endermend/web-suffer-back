// Backend returns 400 (not 401) for an expired/invalid access token — see
// invalid_access_tocken_handler in presentation/api/exception_handlers/auth.py.
// Every apiClient response interceptor needs to recognize this case too, or a
// refresh never fires and requests keep failing with 400 once the token expires.
export function isExpiredAccessTokenError(error: any): boolean {
  if (error.response?.status === 401) return true
  return error.response?.status === 400 && error.response?.data?.detail === 'Invalid access token'
}
