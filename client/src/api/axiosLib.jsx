import axios from "axios";
/**
 * axiosLib.jsx
 * ----------
 * This file sets up and exports a custom configured Axios instance (`api`) for making 
 * HTTP requests.
 * It includes automatic handling of access tokens and token refresh logic for secure
 * API interactions.
 *
 * Functionality:
 * - Sets a default `baseURL` for all API calls (`http://localhost:8081` — update as needed).
 * - Adds a default `Content-Type: application/json` header to all requests.
 * - Applies a 10-second timeout to all requests.
 * 
 * Request Interceptor:
 * - Attaches the access token from `localStorage` to the `Authorization` header if 
 *   available.
 *
 * Response Interceptor:
 * - Automatically handles `401 Unauthorized` responses.
 * - If an access token has expired, it attempts to refresh it using the stored 
 *   `refresh_token`.
 * - If the refresh is successful, it retries the original request with the new token.
 * - If refresh fails, it clears localStorage and optionally redirects the user to the login page.
 *
 * Usage:
 * Instead of using Axios directly, import and use this `api` instance in your services or components:
 * 
 * ```js
 * import api from "./axios";
 * 
 * api.get("/users")
 *    .then(response => console.log(response.data))
 *    .catch(error => console.error(error));
 * ```
 *
 * Note:
 * Be sure your backend is configured to support access/refresh token workflows as implemented here.
 */


// Create and export the custom axios instance
const api = axios.create({
  baseURL: "http://192.168.1.166:5000/api/v1/", // Update this to your actual API base URL
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000,
});

// Request interceptor: add access token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor: handle 401 and refresh token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem("refresh_token");

        const res = await axios.post("http://192.168.1.166:5000/api/v1/auth/refresh-token", {
          refresh_token: refreshToken,
        });

        const newAccessToken = res.data.access_token;

        localStorage.setItem("access_token", newAccessToken);

        // Update headers
        api.defaults.headers.common.Authorization = `Bearer ${newAccessToken}`;
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

        return api(originalRequest);
      } catch (refreshError) {
        console.error("Token refresh failed:", refreshError);
        localStorage.clear();
        window.location.href = "/login"; // optional redirect to login
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
