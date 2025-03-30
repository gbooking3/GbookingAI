import React, { useState } from "react";
import "./AddUser.css"; // Importing the CSS file for styling
import NotRegistered from "./adduser"; // Importing NotRegistered component

const API_URL = import.meta.env.VITE_API_URL;

function Login() {
  const [ownid, setOwnID] = useState(""); // State for ownid
  const [phone, setPhone] = useState(""); // State for phone
  const [loading, setLoading] = useState(false); // Loading state
  const [errorMessage, setErrorMessage] = useState(""); // Error message
  const [isNotRegistered, setIsNotRegistered] = useState(false); // For checking if user is registered

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent the form from reloading the page
    setLoading(true); // Set loading state to true
    setErrorMessage(""); // Reset error message
    setIsNotRegistered(false); // Reset 'Not Registered' state

    const loginData = { ownid, phone }; // Data to send

    try {
      // Sending a POST request with login data to the server
      const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(loginData), // Send the loginData object
      });

      // Check if the response is not okay (status not in 200-299 range)
      if (!response.ok) {
        if (response.status === 404) {
          setIsNotRegistered(true); // User not found, show 'Not Registered' message
          return;
        } else {
          throw new Error("Invalid credentials"); // Handle other errors
        }
      }

      // If login is successful, clear input fields and show success message
      alert("Login successful!");
      setOwnID(""); // Reset ownid input
      setPhone(""); // Reset phone input
    } catch (error) {
      console.error("Error:", error); // Log the error
      setErrorMessage(error.message); // Show error message on UI
    } finally {
      setLoading(false); // Set loading state to false
    }
  };

  return (
    <div className="form-container">
      {isNotRegistered ? (
        <NotRegistered /> // Show NotRegistered component if user isn't found
      ) : (
        <form onSubmit={handleSubmit} className="form">
          <h2 className="form-title">Gbooking Login</h2>
          {errorMessage && <p className="error-message">{errorMessage}</p>}
          <div className="form-inputs">
            <input
              type="text"
              value={ownid}
              onChange={(e) => setOwnID(e.target.value)} // Capture ownid input
              placeholder="Your ID"
              required
              className="form-input"
            />
            <input
              type="text" // Change from "phone" to "text" for input type consistency
              value={phone}
              onChange={(e) => setPhone(e.target.value)} // Capture phone input
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
