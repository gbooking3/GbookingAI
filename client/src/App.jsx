import { BrowserRouter, Routes, Route } from "react-router-dom";
import SignupPage from "./pages/website/auth/signup/SignupPage";
import LoginPage from "./pages/website/auth/login/LoginPage"
import HomePage from "./pages/home/HomePage"

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage />}/>
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/home" element={<HomePage />} />
      </Routes>
    </BrowserRouter>
  );
}