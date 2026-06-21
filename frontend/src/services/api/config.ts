const API_BASE_URL = 'http://localhost:8000'

// GET /api/download/{filename} carries no "JWT Authentication" entry in openapi.json,
// so it's reachable with a plain <a href> — no need to route it through apiClient.
// tasks_store.ts uses this to turn a submission's bare stored filename into a clickable link.
export function buildDownloadUrl(filename: string): string {
  return `${API_BASE_URL}/api/download/${encodeURIComponent(filename)}`
}
