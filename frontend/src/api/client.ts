// Native fetch wrapper with CSRF token bootstrapping and cookie session support

let cachedCsrfToken: string | null = null;
const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '');

function getCookie(name: string): string | null {
  if (typeof document === 'undefined') return null;
  const match = document.cookie.match(new RegExp('(^|;\\s*)(' + name + ')=([^;]*)'));
  return match ? decodeURIComponent(match[3]) : null;
}

export async function fetchCsrfToken(): Promise<string> {
  const cookieToken = getCookie('csrftoken');
  if (cookieToken) {
    cachedCsrfToken = cookieToken;
    return cookieToken;
  }
  try {
    const res = await fetch(`${API_BASE_URL}/api/auth/csrf/`, { credentials: 'include' });
    if (res.ok) {
      const data = await res.json();
      if (data.csrftoken) {
        cachedCsrfToken = data.csrftoken;
        return data.csrftoken;
      }
    }
  } catch (err) {
    console.warn('Failed to fetch CSRF token:', err);
  }
  return cachedCsrfToken || '';
}

export async function apiClient<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const path = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  const url = `${API_BASE_URL}${path}`;
  const headers = new Headers(options.headers || {});

  if (!headers.has('Content-Type') && !(options.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json');
  }

  // State-changing requests require CSRF token
  const method = (options.method || 'GET').toUpperCase();
  if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
    const token = getCookie('csrftoken') || cachedCsrfToken || (await fetchCsrfToken());
    if (token) {
      headers.set('X-CSRFToken', token);
    }
  }

  const response = await fetch(url, {
    ...options,
    headers,
    credentials: 'include', // send session cookies across same-origin
  });

  if (response.status === 204) {
    return {} as T;
  }

  const contentType = response.headers.get('content-type');
  const isJson = contentType && contentType.includes('application/json');
  const data = isJson ? await response.json() : await response.text();

  if (!response.ok) {
    const errorMsg =
      (typeof data === 'object' && data !== null && 'detail' in data && typeof (data as { detail: unknown }).detail === 'string'
        ? (data as { detail: string }).detail
        : typeof data === 'object'
        ? JSON.stringify(data)
        : String(data)) || `HTTP error ${response.status}`;

    const error = new Error(errorMsg) as Error & { status: number; data: unknown };
    error.status = response.status;
    error.data = data;
    throw error;
  }

  return data as T;
}
