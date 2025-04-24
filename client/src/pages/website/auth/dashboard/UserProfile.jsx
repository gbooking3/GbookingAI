/* eslint-disable no-unused-vars */
import { useContext, useState, useEffect } from "react";
import { User } from "../../context/UserContext";
import { useLocation, useNavigate } from "react-router-dom";

import InputField from '../../../../components/input_field/InputField';
import useInput from '../../../../hooks/useFormInput';
import { REGEX, REGEX_MESSAGES, ROUTE_PATHS } from '../../../../utils/consts';
import Cookies from "universal-cookie";
import './ProfilePage.css'; 
import { apiDelete } from "../../../../api/apiMethods";

import Loading from "../../../../components/loading/Loading";
function ProfilePage() {
  const navigate = useNavigate();
  const userContext = useContext(User);
  const user = userContext?.auth?.userDetails || {};

  const userName = useInput(user.name || "", REGEX.NAME, REGEX_MESSAGES.NAME);
  const userEmail = useInput(user.email || "", REGEX.EMAIL, REGEX_MESSAGES.EMAIL);
  const userPhone = useInput(user.phone || "", REGEX.PHONE, REGEX_MESSAGES.PHONE);
  const userId = useInput(user.ownid || "", REGEX.ID, REGEX_MESSAGES.ID);

  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [deleteInput, setDeleteInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const location = useLocation();
  useEffect(() => {
      const cookies = new Cookies();
      const accessToken = cookies.get("access_token");
    
      const isOnDashboard = location.pathname === ROUTE_PATHS.MAIN.PROFILE;
    
      if (!accessToken && isOnDashboard) {
        userContext.setAuth(null); // Clear any existing user context
        navigate(ROUTE_PATHS.AUTH.LOGIN, {
          replace: true,
        });
      }
    }, [location.pathname, navigate, userContext]);


  const handleSave = () => {
    const updatedUser = {
      name: userName.value,
      email: userEmail.value,
      phone: userPhone.value,
      ownid: userId.value
    };
    console.log("Saving changes:", updatedUser);
    alert("Changes saved successfully!");
  };

  const handleDeleteClick = () => {
    setShowDeleteConfirm(true);
    setDeleteInput("");
  };

  const confirmDelete = async () => {
    try {
      const res = await apiDelete('auth/delete-account', { ownid: userId.value });
  
      if (res && res.message === "User deleted successfully.") {
        // ✅ Remove cookies
        const cookies = new Cookies();
        cookies.remove("access_token", { path: "/" });
        cookies.remove("refresh_token", { path: "/" });
  
        // ✅ Reset context
        userContext.setAuth(null);
  
        // ✅ Redirect user
        alert("Account deleted successfully.");
            
        navigate(ROUTE_PATHS.AUTH.LOGIN, {
          replace: true
        });
      } else {
        alert(res?.error || "Failed to delete account.");
      }
    } catch (error) {
      console.error("Delete error:", error);
      alert("An error occurred while deleting your account.");
    }
  };
  
  
  if (isLoading) {
    return <Loading />;
  }
  return (
    <div style={{ display: "flex", minHeight: "100vh", fontFamily: "Arial, sans-serif" }}>
      {/* Sidebar */}
      <div style={{
        width: "220px",
        backgroundColor: "#0d47a1",
        color: "#fff",
        padding: "24px",
        display: "flex",
        flexDirection: "column",
        gap: "24px"
      }}>
        <h2>☰ Menu</h2>
        <div onClick={() => navigate("/dashboard")} style={{ cursor: "pointer" }}>📊 Dashboard</div>
        <div onClick={() => navigate("/profile")} style={{ cursor: "pointer" }}>👤 Profile</div>
        <div onClick={() => navigate("/login")} style={{ cursor: "pointer" }}>🔓 Logout</div>
        <div onClick={() => navigate("/history")} style={{ cursor: "pointer" }}>🕓 History</div>
      </div>

      {/* Main Content */}
      <div style={{ flex: 1, padding: "40px", backgroundColor: "#f1f6fb" }}>
        <h1 style={{ textAlign: "center", fontSize: "32px", color: "#0d47a1", marginBottom: "24px" }}>
          👤 Edit Profile
        </h1>

        <div style={{
          backgroundColor: "#ffffff",
          padding: "32px",
          borderRadius: "12px",
          maxWidth: "900px",
          margin: "0 auto",
          boxShadow: "0 4px 12px rgba(0,0,0,0.1)"
        }}>
          <div style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: "24px",
            marginBottom: "32px"
          }}>
            <InputField type="text" label="Full Name" {...userName} />
            <InputField type="email" label="Email" {...userEmail} disabled={true} />
            <InputField type="tel" label="Phone" {...userPhone} disabled={true} />
            <InputField type="text" label="ID" {...userId} disabled={true} />
          </div>
          <p style={{
            color: "#d32f2f",
            backgroundColor: "#fff3cd",
            padding: "12px 16px",
            borderRadius: "8px",
            border: "1px solid #ffeeba",
            fontSize: "14px",
            maxWidth: "900px",
            margin: "0 auto 24px",
            textAlign: "center"
          }}>
            <strong>Need to update your Email, Phone, or ID?</strong><br />
            For security reasons, please reach out via the 
            <button
              onClick={() => {
                setIsLoading(true);
                setTimeout(() => {
                  navigate("/contact");
                }, 1500); // 1.5s loading screen
              }}
              style={{
                color: "#0d47a1",
                textDecoration: "underline",
                background: "none",
                border: "none",
                cursor: "pointer",
                fontWeight: "bold",
                padding: 0
              }}
            >
              Contact Us
            </button>
            page and our support team will assist you.
          </p>


          {/* Buttons */}
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <button
              onClick={handleSave}
              className="save-button"
            >
              💾 <span>Save Changes</span>
            </button>

            <button
              onClick={handleDeleteClick}
              className="delete-button"
            >
              🗑️ <span>Delete Account</span>
            </button>
          </div>
        </div>
      </div>

      {/* Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="modal-backdrop">
          <div className="modal-box">
            <h4>Confirm Account Deletion</h4>
            <p>Type <strong>delete</strong> to confirm:</p>
            <input
              type="text"
              value={deleteInput}
              onChange={(e) => setDeleteInput(e.target.value)}
              placeholder="Type 'delete'"
              className="delete-input"
            />
            <div className="modal-buttons">
              <button className="cancel-btn" onClick={() => setShowDeleteConfirm(false)}>Cancel</button>
              <button
                className="confirm-btn"
                disabled={deleteInput.trim().toLowerCase() !== "delete"}
                onClick={confirmDelete}
              >
                Confirm Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default ProfilePage;
