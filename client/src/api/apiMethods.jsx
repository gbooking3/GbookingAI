/* eslint-disable no-useless-catch */
import api from "./axiosLib";


/**
 * API Utility Functions
 * ---------------------
 * This module exports reusable helper functions for making HTTP requests using 
 * the custom Axios instance (`api`). It wraps the standard HTTP methods (GET, 
 * POST, PUT, DELETE) for consistent and clean usage throughout your app.
 *
 * Functionality:
 * - `apiGet(url, config)`: Performs a GET request to the specified URL with optional Axios config.
 * - `apiPost(url, data, config)`: Sends a POST request with data and optional config.
 * - `apiPut(url, data, config)`: Sends a PUT request with data and optional config.
 * - `apiDelete(url, config)`: Sends a DELETE request to the specified URL with optional config.
 *
 * Each function:
 * - Uses the `api` instance, which is pre-configured for token handling and base URL (see `axios.jsx`).
 * - Returns the `.data` field of the Axios response.
 * - Catches and rethrows errors for centralized error handling elsewhere in the app.
 *
 * Usage example:
 * ```js
 * import { apiGet, apiPost } from './apiUtils';
 *
 * const fetchUser = async () => {
 *   try {
 *     const user = await apiGet('/user/profile');
 *     console.log(user);
 *   } catch (err) {
 *     console.error('Failed to fetch user', err);
 *   }
 * };
 * ```
 */



// GET request
export const apiGet = async (url, config = {}) => {
  try {
    const response = await api.get(url, config);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// POST request
export const apiPost = async (url, data = {}, config = {}) => {
  try {
    const response = await api.post(url, data, config);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// PUT request
export const apiPut = async (url, data = {}, config = {}) => {
  try {
    const response = await api.put(url, data, config);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// DELETE request
export const apiDelete = async (url, data = {}, config = {}) => {
  try {
    const response = await api.delete(url, {
      data, // 🔥 Axios supports body this way
      ...config,
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

