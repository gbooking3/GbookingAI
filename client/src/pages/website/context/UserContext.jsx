/* eslint-disable react/prop-types */
import { createContext, useState } from "react";

/**
 * UserContext.jsx
 * ----------------
 * This file defines a React context for managing user authentication state 
 * throughout the application.
 * 
 * Functionality:
 * - Creates a `User` context using React's `createContext`, initialized with
 *   an empty object.
 * - Exports a `UserProvider` component that wraps its children with the context
 *   provider.
 * - Inside the provider, it uses `useState` to manage the `auth` state, which
 *   typically holds user authentication details.
 * - Exposes both `auth` (the user data) and `setAuth` (a function to update
 *   the user data) to the rest of the app.
 * 
 */


export const User = createContext({});

export default function UserProvider({ children }) {
  const [auth, setAuth] = useState(() => {
    const access_token = localStorage.getItem("access_token");
    const userDetails = localStorage.getItem("user_details");
    return access_token ? { access_token, userDetails: JSON.parse(userDetails) } : {};
  });
  
  return <User.Provider value={{ auth, setAuth }}>{children}</User.Provider>;
}