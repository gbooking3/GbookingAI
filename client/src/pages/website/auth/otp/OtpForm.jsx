import { useState, useContext, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { User } from "../../context/UserContext";
import Cookies from "universal-cookie";
import { apiPost } from "../../../../api/apiMethods";
import Loading from "../../../../components/loading/Loading";
import { ROUTE_PATHS, API_ENDPOINTS } from '../../../../utils/consts';

function OTPForm() {
  const location = useLocation();
  const navigate = useNavigate();
  const userContext = useContext(User);

  const isAccessible = location.state?.accessible;

  const [otp, setOtp] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  // Redirect to login if accessed directly
  useEffect(() => {
    if (!isAccessible) {
      navigate(ROUTE_PATHS.AUTH.LOGIN, { replace: true });
    }
  }, [isAccessible, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMessage("");

    try {
      const response = await apiPost(API_ENDPOINTS.AUTH.VERIFY_OTP, { otp });

      userContext.setAuth((prev) => ({
        ...prev,
        isVerified: true,
      }));

      navigate(ROUTE_PATHS.MAIN.DASHBOARD, { replace: true });

    } catch (error) {
      if (error.response?.status === 400) {
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
      {isAccessible ? (
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
              Didn’t receive the code? <a href={API_ENDPOINTS.AUTH.RESEND_OTP}>Resend OTP</a>
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
