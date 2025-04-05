import { useContext } from "react";
import { User } from "../../context/UserContext";
import { Navigate, Outlet, useLocation } from "react-router-dom";

/**
 * RequiredAuth.jsx
 * ----------------
 * This component is used to protect specific routes in a React application 
 * that uses `react-router-dom` v6+.
 * It ensures that only authenticated users can access certain parts of the app.
 *
 * Functionality:
 * - It uses the React `useContext` hook to access the user's authentication 
 *      state from a custom UserContext.
 * - It uses the `useLocation` hook to store the current location, enabling 
 *      redirection back to the attempted path after login.
 * - If the user is authenticated (`user.auth.userDetails` exists), it renders 
 *      the requested child route using `<Outlet />`.
 * - If not authenticated, it redirects the user to the home page (`/`) and passes
 *       the intended location using `state`.
 *
 * Typical use case:
 * This component is used as a wrapper in your route definitions for paths that require authentication.
 * 
 * Example usage in App.jsx or router config:
 * <Route element={<RequireAuth />}>
 *   <Route path="/dashboard" element={<Dashboard />} />
 * </Route>
 */


export default function RequireAuth() {
    const user = useContext(User);
    const location = useLocation();
  
    return user.auth.userDetails ? (
      <Outlet />
    ) : (
      <Navigate state={{ from: location }} replace to="/" />
    );
  }
  