import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import SignupPage from "./pages/website/auth/signup/SignupPage";
import LoginPage from "./pages/website/auth/login/LoginPage";
import HomePage from "./pages/home/HomePage";
import OtpPage from "./pages/website/auth/otp/OtpPage";
import DashBoard from "./pages/website/auth/dashboard/DashBoard";
import Profile from "./pages/website/auth/dashboard/UserProfile";

import PersistLogin from "./pages/website/auth/login/PersistLogin";
import RequireAuth from "./pages/website/auth/login/RequireAuth";
import UserProvider from "./pages/website/context/UserContext"; 

import NotFoundPage from './missing/NotFoundPage'
import {ROUTE_PATHS} from './utils/consts'

export default function App() {
  return (
    <UserProvider> 
      <BrowserRouter>
        <Routes>
          {/* Redirect root (/) to /login */}
          <Route path={ROUTE_PATHS.MAIN.HOME} element={<Navigate to={ROUTE_PATHS.AUTH.LOGIN} replace />} />
          {/* public routes */}
          
          {/* Auth */}
          <Route path={ROUTE_PATHS.AUTH.LOGIN}  element={<LoginPage />} />
          <Route path={ROUTE_PATHS.AUTH.SIGNUP} element={<SignupPage />} />
          <Route path={ROUTE_PATHS.AUTH.OTP}    element={<OtpPage />} />

          {/* Protected Routes */}
          <Route element={<PersistLogin />}>
            <Route element={<RequireAuth />}>

              <Route path={ROUTE_PATHS.MAIN.HOME}      element={<HomePage />} />
              <Route path={ROUTE_PATHS.MAIN.DASHBOARD} element={<DashBoard />} />
              <Route path={ROUTE_PATHS.MAIN.PROFILE}   element={<Profile />} />

              
            </Route>
          </Route>

          {/* Errors */}
          {/* catch all */}
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </BrowserRouter>
    </UserProvider>
  );
}
