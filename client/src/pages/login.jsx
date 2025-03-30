import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import "./AddUser.css";
import NotRegistered from "./adduser";

const API_URL = import.meta.env.VITE_API_URL;

function Login() {
  const [ownid, setOwnID] = useState("");
  const [phone, setPhone] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [isNotRegistered, setIsNotRegistered] = useState(false);
  
  const navigate = useNavigate(); // Initialize navigate function

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMessage("");
    setIsNotRegistered(false);

    const loginData = { ownid, phone };

    try {
      const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(loginData),
      });

      if (!response.ok) {
        if (response.status === 404) {
          alert("User Not Founded");
          return;
        } else {
          throw new Error("Invalid credentials");
        }
      }

      alert("Login successful!");
      setOwnID("");
      setPhone("");

      // **Redirect to Home page after successful login**
      navigate("/home"); 

    } catch (error) {
      console.error("Error:", error);
      setErrorMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      {isNotRegistered ? (
        <div className="not-registered">
          <p className="error-message">User not registered.</p>
          <a href="/signup" className="form-button">Sign Up Here</a>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="form">
          <h2 className="form-title">Gbooking Login</h2>
          {errorMessage && <p className="error-message">{errorMessage}</p>}
          <div className="form-inputs">
            <input
              type="text"
              value={ownid}
              onChange={(e) => setOwnID(e.target.value)}
              placeholder="Your ID"
              required
              className="form-input"
            />
            <input
              type="text"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="Phone"
              required
              className="form-input"
            />
          </div>
          <button type="submit" className="form-button" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
          <p className="signup-link">
            Not registered? <a href="/signup">Sign up here</a>
          </p>
        </form>
      )}
    </div>
  );
}

export default Login;
