import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import SignupPage from "./pages/website/auth/signup/SignupPage";
import LoginPage from "./pages/website/auth/login/LoginPage";
import HomePage from "./pages/home/HomePage";
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
          <Route element={<PersistLogin />}>
            <Route element={<RequireAuth />}>
              <Route path="/home" element={<HomePage />} />
            </Route>
          </Route>
        </Routes>
      </BrowserRouter>
    </UserProvider>
  );
}
