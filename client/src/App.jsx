import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import SignupPage from "./pages/website/auth/signup/SignupPage";
import LoginPage from "./pages/website/auth/login/LoginPage";
import HomePage from "./pages/home/HomePage";
import OtpPage from "./pages/website/auth/otp/OtpPage";
import DashBoard from "./pages/website/auth/dashboard/DashBoard";

import PersistLogin from "./pages/website/auth/login/PersistLogin";
import RequireAuth from "./pages/website/auth/login/RequireAuth";
import UserProvider from "./pages/website/context/UserContext"; 

export default function App() {
  return (
    <UserProvider> 
      <BrowserRouter>
        <Routes>
          {/* Redirect root (/) to /login */}
          <Route path="/" element={<Navigate to="/login" replace />} />

          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/otp" element={<OtpPage />} />
          <Route element={<PersistLogin />}>
            <Route element={<RequireAuth />}>

              <Route path="/home" element={<HomePage />} />
              <Route path="/dashboard" element={<DashBoard />} />

              
            </Route>
          </Route>
        </Routes>
      </BrowserRouter>
    </UserProvider>
  );
}
