import React, { useState } from "react";
import "./AddUser.css"; // Importing the CSS file for styling
import NotRegistered from "./adduser"; // Importing NotRegistered component

const API_URL = import.meta.env.VITE_API_URL;

function Login() {
  const [ownid, setOwnID] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [isNotRegistered, setIsNotRegistered] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMessage("");
    setIsNotRegistered(false);

    const loginData = { ownid, password };

    try {
      const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(loginData),
      });

      if (!response.ok) {
        if (response.status === 404) {
          setIsNotRegistered(true);
          return;
        } else {
          throw new Error("Invalid credentials");
        }
      }

      alert("Login successful!");
      setOwnID("");
      setPassword("");
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
        <NotRegistered />
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
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              required
              className="form-input"
            />
          </div>
          <button type="submit" className="form-button" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
          <p className="signup-link">Not registered? <a href="/signup">Sign up here</a></p>
        </form>
      )}
    </div>
  );
}

export default Login;
