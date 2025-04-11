import { useContext } from "react";
import { User } from '../../context/UserContext'; // Make sure path is correct
import { useNavigate } from 'react-router-dom'; // Import useNavigate

function ProfilePage() {
  const navigate = useNavigate(); // Initialize the navigate function

  // 👤 Get user info from context
  const userContext = useContext(User);
  const user = userContext?.auth?.userDetails || {};

  // Navigate to Dashboard when clicked
  const handleDashboardClick = () => {
    navigate("/dashboard");
  };

  // Handle profile click to navigate to profile page
  const handleLogoutClick = () => {
    navigate("/login");
  };

  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      
      {/* Sidebar */}
      <div style={{
        width: "200px",
        backgroundColor: "#0d47a1",
        color: "#fff",
        padding: "20px",
        display: "flex",
        flexDirection: "column",
        gap: "20px",
        fontSize: "16px"
      }}>
        <h3>☰ Menu</h3>
        {/* Dashboard button navigates to dashboard page */}
        <div onClick={handleDashboardClick} style={{ cursor: "pointer" }}>📊 Dashboard</div>
        <div style={{ cursor: "pointer" }} onClick={() => navigate("/profile")}>👤 Profile</div>
        <div onClick={handleLogoutClick} style={{ cursor: "pointer" }}>🔓 Logout</div>

      </div>

      {/* Profile content area */}
      <div className="profile-container" style={{ flex: 1, padding: "40px" }}>
        <div className="profile">
          <h2 className="profile-title">User Profile</h2>

          {/* 👤 User profile card */}
          <div style={{
            backgroundColor: "#e3f2fd",
            padding: "12px 16px",
            borderRadius: "10px",
            marginBottom: "16px",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            fontSize: "14px",
            color: "#333",
            boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
          }}>
            <div>
              <b>{"Name: "+user.name || "No Name"}</b><br />
              <span>{"Email: " +user.email || "No Email"}</span><br />
              <span>{"Phone Number: " + user.phone || "No Phone"}</span><br />
              <span>{"ID: " +user.ownid || "No ID"}</span>

            </div>
            <span style={{ fontSize: "24px" }}>👤</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProfilePage;
