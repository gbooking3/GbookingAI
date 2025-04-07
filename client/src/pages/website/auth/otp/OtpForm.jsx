import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { User } from "../../context/UserContext";
import { apiPost } from "../../../../api/apiMethods";

function OTPForm() {
  const [otp, setOtp] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const userContext = useContext(User);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMessage("");

    try {
      const response = await apiPost("auth/verifyotp", { otp });
      userContext.setAuth((prev) => ({
        ...prev,
        isVerified: true,
      }));

      alert("OTP Verified!");
      navigate("/dashboard");
    } catch (error) {
      if (error.response && error.response.status === 400) {
        setErrorMessage("Invalid OTP. Please try again.");
      } else {
        console.error("OTP verification error:", error);
        setErrorMessage("Something went wrong. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
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
          Didn’t receive the code? <a href="/resend-otp">Resend OTP</a>
        </p>
      </form>
    </div>
  );
}

export default OTPForm;
