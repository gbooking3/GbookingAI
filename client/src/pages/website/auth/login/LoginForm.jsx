import { useState, useContext, useRef, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import Cookies from "universal-cookie";
import { User } from '../../context/UserContext';
import "./LoginPage.css";
import { apiPost } from '../../../../api/apiMethods';
import InputField from '../../../../components/input_field/InputField';
import Auth_Button from '../../../../components/button/Auth_Button';
import ContactMethodSelector from '../../../../components/selector/ContactMethodSelector';
import useInput from '../../../../hooks/useFormInput';
import {
  REGEX,
  REGEX_MESSAGES,
  ROUTE_PATHS,
  API_ENDPOINTS
} from '../../../../utils/consts';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCircleCheck } from "@fortawesome/free-solid-svg-icons";

function LoginForm() {
  const [contactMethod, setContactMethod] = useState("email");
  const errRef = useRef();
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [isNotRegistered, setIsNotRegistered] = useState(false);

  const userContext = useContext(User);
  const navigateTo = useNavigate();
  const location = useLocation();

  const isRegistered = location.state?.registered || false;
  const isReactivated = location.state?.reactivated || false;
  const isLoggedOut = location.state?.logged_out || false;

  const userId = useInput(location.state?.ownid || "", REGEX.ID, REGEX_MESSAGES.ID);
  const cookies = new Cookies();

  // ✅ Redirect to dashboard if already logged in
  useEffect(() => {
    const accessToken = cookies.get("access_token");
    if (accessToken) {
      navigateTo(ROUTE_PATHS.MAIN.DASHBOARD, { replace: true });
    }

    // Optional: Clear the state message after first load
    window.history.replaceState({}, document.title);
  }, [navigateTo]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage("");
    setLoading(true);
    setIsNotRegistered(false);

    const loginData = {
      ownid: userId.value,
      method: contactMethod,
    };

    try {
      const response = await apiPost(API_ENDPOINTS.AUTH.LOGIN, loginData);
      const { access_token, refresh_token, user_details } = response;

      cookies.set("access_token", access_token, { path: "/" });
      cookies.set("refresh_token", refresh_token, { path: "/" });

      userContext.setAuth({
        access_token,
        refresh_token,
        userDetails: user_details,
      });

      navigateTo(ROUTE_PATHS.AUTH.OTP, {
        state: { ownid: userId.value, accessible: true },
        replace: true,
      });
    } catch (error) {
      if (!error?.response) {
        setErrorMessage("No Server Response");
      } else if (error.response?.status === 404) {
        const errMSG = error.response.data?.error;
        setErrorMessage(errMSG || "Something went wrong");
      } else {
        setErrorMessage("Login failed. Please try again.");
      }
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
        <>
          <form onSubmit={handleSubmit} className="form">
            {isRegistered && (
              <p className="successmsg">
                Registered successfully! Please log in below
                <FontAwesomeIcon icon={faCircleCheck} style={{ fontSize: "20px", color: "green", marginLeft: "10px" }} />
              </p>
            )}

            {isReactivated && (
              <p className="successmsg">
                Account reactivated! Please log in.
                <FontAwesomeIcon icon={faCircleCheck} style={{ fontSize: "20px", color: "green", marginLeft: "10px" }} />
              </p>
            )}

            {isLoggedOut && (
              <p className="successmsg">
                Logged out successfully.
                <FontAwesomeIcon icon={faCircleCheck} style={{ fontSize: "20px", color: "green", marginLeft: "10px" }} />
              </p>
            )}

            <h2 className="form-title">Gbooking Login</h2>
            <p
              ref={errRef}
              className={errorMessage ? "errmsg" : "offscreen"}
              aria-live="assertive"
            >
              {errorMessage}
            </p>

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
              <ContactMethodSelector method={contactMethod} setMethod={setContactMethod} />
            </div>

            <Auth_Button
              validation={userId.valid}
              name="Login"
              loading={loading}
            />

            <p className="signup-link">
              Not registered? <a href="/signup">Sign-up</a>
            </p>
          </form>
        </>
      )}
    </div>
  );
}

export default LoginForm;
