/* eslint-disable no-unused-vars */
import { useState, useRef, useContext, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import './SignupPage.css';
import { apiPost } from '../../../../api/apiMethods';
import InputField from '../../../../components/input_field/InputField'
import Auth_Button from '../../../../components/button/Auth_Button'
import useInput from '../../../../hooks/useFormInput'
import {REGEX, REGEX_MESSAGES, ROUTE_PATHS, API_ENDPOINTS} from '../../../../utils/consts'
import Cookies from "universal-cookie";

import { User } from '../../context/UserContext';

const API_URL = import.meta.env.VITE_API_URL;

function SignupForm() {
  const { auth } = useContext(User);
  const navigate = useNavigate();

  useEffect(() => {
    const cookies = new Cookies();
    const accessToken = cookies.get("access_token");
  
    if (accessToken) {
      navigate(ROUTE_PATHS.MAIN.DASHBOARD, { replace: true });
    }
  }, []);
  


  const errRef = useRef();
  const [errMsg, setErrMsg] = useState("");

  const navigateTo = useNavigate(); 


  const userId    = useInput("", REGEX.ID   , REGEX_MESSAGES.ID   );
  const userEmail = useInput("", REGEX.EMAIL, REGEX_MESSAGES.EMAIL);
  const userPhone = useInput("", REGEX.PHONE, REGEX_MESSAGES.PHONE);
  const userName  = useInput("", REGEX.NAME , REGEX_MESSAGES.NAME );
  
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  /**
 * Validates an Israeli ID number using the official checksum algorithm.
 * @param {string | number} id - The ID number as a string or number.
 * @returns {boolean} True if the ID is valid, false otherwise.
 */

  const  validateIsraeliID = (id) => {
    // Convert to string and remove any whitespace
    id = String(id).trim();

    // ID must be 5 to 9 digits
    if (!/^\d{5,9}$/.test(id)) return false;

    // Pad with leading zeros if less than 9 digits
    id = id.padStart(9, '0');

    let sum = 0;

    for (let i = 0; i < 9; i++) {
      let digit = Number(id[i]);
      let multiplied = digit * ((i % 2) + 1);

      // If the result is more than 9, subtract 9 (same as adding the digits)
      if (multiplied > 9) multiplied -= 9;

      sum += multiplied;
    }

    return sum % 10 === 0;
  }

  const handleSubmit = async (e) => {
    try {
      setErrMsg("");
      e.preventDefault();
      setLoading(true);
      setErrorMessage("");
  
      if (
        !userId.valid ||
        !userEmail.valid ||
        !userPhone.valid ||
        !userName.valid
      ) {
        setErrMsg("Invalid Entry");
        return;
      }
  
      if (!validateIsraeliID(userId.value)) {
        setErrMsg("Not Valid ID Number.");
        return;
      }
  
      const user = {
        ownid: userId.value,
        email: userEmail.value,
        phone: userPhone.value,
        name: userName.value,
        clientid:1
      };
  
      const response = await apiPost(API_ENDPOINTS.AUTH.SIGNUP, user);
  
      const message = response?.message || "";
  
      if (message.includes("reactivated")) {
        // 🔁 Navigate with reactivated flag
        navigateTo(ROUTE_PATHS.AUTH.LOGIN, {
          state: { ownid: userId.value, reactivated: true },
          replace: true,
        });
      } else {
        // 🆕 Navigate with registered flag
        navigateTo(ROUTE_PATHS.AUTH.LOGIN, {
          state: { ownid: userId.value, registered: true },
          replace: true,
        });
      }
  
    } catch (err) {
      if (!err?.response) {
        setErrMsg("No Server Response");
      } else if (err.response?.status === 400) {
        const errMessage = err.response.data?.error;
        setErrMsg(errMessage || "Something went wrong.");
      } else if (err.response?.status === 403) {
        setErrMsg("An account with this ID already exists but was previously deactivated. Please contact customer service.");
      } else {
        setErrMsg("Registration failed. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };
  

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit} className="form">
        <h2 className="form-title">Gbooking Register</h2>
          <section>
              <p
                ref={errRef}
                className={errMsg ? "errmsg" : "offscreen"}
                aria-live="assertive"
              >
                {errMsg}
              </p>
          <div className="form-inputs">
          <InputField
                type        = "text"
                label       = "Full Name"
                value       = {userName.value}
                onChange    = {userName.handleChange}
                valid       = {userName.valid}
                focus       = {userName.handleFocus}
                blur        = {userName.handleBlur}
                placeholder = ""
                instruction = {userName.instruction}
             
              />
          <InputField
                type        = "email"
                label       = "Email"
                value       = {userEmail.value}
                onChange    = {userEmail.handleChange}
                valid       = {userEmail.valid}
                focus       = {userEmail.handleFocus}
                blur        = {userEmail.handleBlur}
                placeholder = ""
                instruction = {userEmail.instruction}
               
              />
          <InputField
                type        = "tel"
                label       = "Phone"
                value       = {userPhone.value}
                onChange    = {userPhone.handleChange}
                valid       = {userPhone.valid}
                focus       = {userPhone.handleFocus}
                blur        = {userPhone.handleBlur}
                placeholder = ""
                instruction = {userPhone.instruction}
              
              />
          <InputField
                type        = "text"
                label       = "ID"
                value       = {userId.value}
                onChange    = {userId.handleChange}
                valid       = {userId.valid}
                focus       = {userId.handleFocus}
                blur        = {userId.handleBlur}
                placeholder = ""
                instruction = {userId.instruction}
              
              />

          </div>
          <Auth_Button validation={userId.valid && userEmail.valid && userName.valid && userPhone.valid} name="Create Account" loading={loading} />
          
          <p className="m-2">
              Already Registered ?{" "}
              <span className="line">
                <Link to={ROUTE_PATHS.AUTH.LOGIN}>Login</Link>
              </span>
            </p>

        </section>
      </form>
    </div>
  );
}

export default SignupForm;