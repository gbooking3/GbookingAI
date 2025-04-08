import  { useState, useContext } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import Cookies from "universal-cookie";
import { User } from '../../context/UserContext'
import "./LoginPage.css";
import { apiPost } from '../../../../api/apiMethods';


function LoginForm() {
  const [ownid, setOwnID] = useState("");
  const [email, setMail] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [isNotRegistered, setIsNotRegistered] = useState(false);
  const userContext = useContext(User);
  const navigate = useNavigate(); // Initialize navigate function


  // cookie
  const cookie = new Cookies();

  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMessage("");
    setIsNotRegistered(false);

    const loginData = { ownid, email };
    try {
      const response = await apiPost('auth/login', loginData);
    
      const { access_token, refresh_token, user_details } = response;
    
      alert("Login successful!");
      cookie.set("Bearer", access_token);

      cookie.set("access_token", response.access_token);
      cookie.set("refresh_token", response.refresh_token);

      console.log(response)
      userContext.setAuth({
        access_token,
        refresh_token,
        userDetails: user_details,
      });
      navigate("/otp");
    
    } catch (error) {
      if (error.response && error.response.status === 404) {
        alert("User Not Founded");
        setIsNotRegistered(true);
      } else if (error.response && error.response.status === 401) {
        setErrorMessage("Invalid credentials");
      } else {
        console.error("Login error:", error);
        setErrorMessage("Something went wrong. Please try again.");
      }
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

export default LoginForm;
