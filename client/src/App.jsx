import { BrowserRouter, Routes, Route } from "react-router-dom";
import SignupPage from "./pages/website/auth/signup/SignupPage";
import LoginPage from "./pages/website/auth/login/LoginPage"
import HomePage from "./pages/home/HomePage"
import RequireAuth from "./pages/website/auth/login/RequireAuth";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage />}/>
        <Route path="/signup" element={<SignupPage />} />
       
        <Route element={<RequireAuth />} >
          <Route path="/home" element={<HomePage />} />
        </Route>

      </Routes>
    </BrowserRouter>
  );
}