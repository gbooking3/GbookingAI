// LoginFormContainer.js
import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import Cookies from "universal-cookie";
import { User } from "../../context/UserContext";
import { apiPost } from "../../../../api/apiMethods";
import LoginFormUI from "../../../../components/LoginFormUI";

function LoginFormContainer() {
  const [ownid, setOwnID] = useState("");
  const [email, setMail] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [isNotRegistered, setIsNotRegistered] = useState(false);

  const userContext = useContext(User);
  const navigate = useNavigate();
  const cookie = new Cookies();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMessage("");
    setIsNotRegistered(false);

    const loginData = { ownid, email };
    try {
      const response = await apiPost("auth/login", loginData);

      const { access_token, refresh_token, user_details } = response;
      alert("Login successful!");

      cookie.set("Bearer", access_token);
      cookie.set("access_token", access_token);
      cookie.set("refresh_token", refresh_token);

      userContext.setAuth({
        access_token,
        refresh_token,
        userDetails: user_details,
      });

      navigate("/otp");
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
      setLoading(false);
    }
  };

  return (
    <LoginFormUI
      ownid={ownid}
      setOwnID={setOwnID}
      email={email}
      setMail={setMail}
      handleSubmit={handleSubmit}
      loading={loading}
      errorMessage={errorMessage}
      isNotRegistered={isNotRegistered}
    />
  );
}

export default LoginFormContainer;
