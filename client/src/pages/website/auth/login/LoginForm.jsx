import  { useState, useContext } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import Cookies from "universal-cookie";
import { User } from '../../context/UserContext'
import "./LoginPage.css";
import { apiPost } from '../../../../api/apiMethods';
import InputField from '../../../../components/input_field/InputField'
import Auth_Button from '../../../../components/button/Auth_Button'
import useInput from '../../../../hooks/useFormInput'
import {REGEX, REGEX_MESSAGES, ROUTE_PATHS, API_ENDPOINTS} from '../../../../utils/consts'


function LoginForm() {
  // const [ownid, setOwnID] = useState("");
  const [email, setMail] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [isNotRegistered, setIsNotRegistered] = useState(false);
  const userContext = useContext(User);
  const navigate = useNavigate(); // Initialize navigate function

  const userId = useInput("", REGEX.ID, REGEX_MESSAGES.ID);

  // cookie
  const cookie = new Cookies();

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setIsNotRegistered(false);
  
    const loginData = { ownid: userId.value, email };
  
    try {
      const response = await apiPost(API_ENDPOINTS.AUTH.LOGIN, loginData);
  
      const { access_token, refresh_token, user_details } = response;
  
      cookie.set("access_token", access_token);
      cookie.set("refresh_token", refresh_token);
  
      userContext.setAuth({
        access_token,
        refresh_token,
        userDetails: user_details,
      });
  
      navigate( ROUTE_PATHS.AUTH.OTP);

    } catch (error) {
      if (error.response?.status === 404) {
        alert("User Not Found");
        setIsNotRegistered(true);
      } else if (error.response?.status === 401) {
        setErrorMessage("Invalid credentials");
      } else {
        console.error("Login error:", error);
        setErrorMessage("Something went wrong. Please try again.");
      }
    } finally {
      setLoading(false); // 🔥 This ensures loading stops in both success and error
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
            <InputField
              type="text"
              label="Your ID"
              value={userId.value}
              onChange={userId.handleChange}
              valid={userId.valid}
              focus={userId.handleFocus}
              blur={userId.handleBlur}
              placeholder=""
              instruction={userId.instruction}
           
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
          <Auth_Button validation={userId.valid} name="Login" loading={loading} />

          <p className="signup-link">
            Not registered? <a href="/signup">Sign-up</a>
          </p>
        </form>
      )}
    </div>
  );
  
}

export default LoginForm;