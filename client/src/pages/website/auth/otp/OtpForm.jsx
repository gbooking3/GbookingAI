/* eslint-disable no-unused-vars */
import { useState, useContext, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { User } from "../../context/UserContext";
import { apiPost } from "../../../../api/apiMethods";

import Loading from "../../../../components/loading/Loading";
import { ROUTE_PATHS, API_ENDPOINTS} from '../../../../utils/consts'


function OTPForm() {
  const location  = useLocation()
  const navigateTo = useNavigate();

  const [otp, setOtp] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const userContext = useContext(User);

  const [isAccessible, setIsAccessible] = useState(
    location.state && location.state.accessible 
  );

  useEffect(() => {
    if (!location.state || !location.state.accessible) {
      navigateTo(ROUTE_PATHS.AUTH.LOGIN);
    } else {
      setIsAccessible(true);
    }
  }, [location, navigateTo]);

  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMessage("");

    try {
      const response = await apiPost( API_ENDPOINTS.AUTH.VERIFY_OTP, { otp });
      userContext.setAuth((prev) => ({
        ...prev,
        isVerified: true,
      }));

      alert("OTP Verified!");
      navigateTo( ROUTE_PATHS.MAIN.DASHBOARD );
    } catch (error) {
      if (error.response && error.response.status === 400) {
        setErrorMessage(error.response.data?.error);
      } else {
        console.error("OTP verification error:", error);
        setErrorMessage("Something went wrong. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {isAccessible !== null ? (
        <div className="form-container">
          <form onSubmit={handleSubmit} className="form">
            <h2 className="form-title">Verify OTP</h2>
            {errorMessage && <p className="error-message">{errorMessage}</p>}
            <div className="form-inputs">
              <input
                type="text"
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                placeholder="Enter 6-digit OTP"
                maxLength={6}
                required
                className="form-input"
              />
            </div>
            <button type="submit" className="form-button" disabled={loading}>
              {loading ? "Verifying..." : "Verify OTP"}
            </button>
            <p className="signup-link">
              Didn’t receive the code? <a href= { API_ENDPOINTS.AUTH.RESEND_OTP }>Resend OTP</a>
            </p>
          </form>
        </div>
      ) : (
        <Loading />
      )}
    </>
  );
}

export default OTPForm;
