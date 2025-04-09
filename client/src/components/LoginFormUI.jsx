// LoginFormUI.js
import React from "react";

function LoginFormUI({
  ownid,
  setOwnID,
  email,
  setMail,
  handleSubmit,
  loading,
  errorMessage,
  isNotRegistered,
}) {
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
              value={email}
              onChange={(e) => setMail(e.target.value)}
              placeholder="Email"
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

export default LoginFormUI;
