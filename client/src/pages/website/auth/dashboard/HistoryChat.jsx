import { useEffect, useState, useContext } from "react";
import { apiPost } from "../../../../api/apiMethods";
import { User } from "../../context/UserContext";
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import { API_ENDPOINTS, ROUTE_PATHS } from "../../../../utils/consts";


function HistoryChat() {
  const navigateTo = useNavigate(); // Initialize the navigate function

  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);
  const userContext = useContext(User);
  const user = userContext?.auth?.userDetails || {};

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await apiPost(API_ENDPOINTS.MAIN.CHAT_HISTORY, { id: user.ownid });
        setConversations(res.history || []);
        setLoading(false);
      } catch (err) {
        console.error("Failed to fetch chat history", err);
        setLoading(false);
      }
    };

    fetchHistory();
  }, [user.ownid]);

    const handleLogoutClick    = () => navigateTo(ROUTE_PATHS.AUTH.LOGIN);
    const handleProfileClick   = () => navigateTo(ROUTE_PATHS.MAIN.PROFILE);
    const handleDashboardClick = () => navigateTo(ROUTE_PATHS.MAIN.DASHBOARD);
    const handleHistoryClick   = () => navigateTo(ROUTE_PATHS.MAIN.HISTORY);

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
        <div onClick={handleProfileClick} style={{ cursor: "pointer" }}>👤 Profile</div>
        <div onClick={handleLogoutClick} style={{ cursor: "pointer" }}>🔓 Logout</div>
        <div onClick={handleHistoryClick} style={{ cursor: "pointer" }}>🕓 History</div>


      </div>

        <div style={{ padding: "40px", maxWidth: "900px", margin: "auto" }}>
          <h2 style={{ fontSize: "26px", marginBottom: "24px", color: "#0d47a1" }}>
            🕓 Chat History
          </h2>

          {loading ? (
            <p>Loading...</p>
          ) : conversations.length === 0 ? (
            <p>No chat history found.</p>
          ) : (
            conversations.map((conv, index) => (
              <div
                key={conv._id || index}
                style={{
                  border: "1px solid #ccc",
                  borderRadius: "16px",
                  padding: "24px",
                  marginBottom: "24px",
                  backgroundColor: "#e3f2fd",
                  boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
                }}
              >
                <h4 style={{ color: "#0d47a1", marginBottom: "16px" }}>
                  🗂️ Conversation #{conversations.length - index} –{" "}
                  {new Date(conv.created_at).toLocaleString()}
                </h4>

                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "10px",
                    paddingLeft: "12px",
                  }}
                >
                  {conv.messages.map((msg, i) => (
                    <div
                      key={i}
                      style={{
                        alignSelf: msg.from === "bot" ? "flex-start" : "flex-end",
                        backgroundColor:
                          msg.from === "bot" ? "#f1f1f1" : "#bbdefb",
                        padding: "12px 16px",
                        borderRadius: "18px",
                        maxWidth: "75%",
                        textAlign: msg.from === "bot" ? "left" : "right",
                        boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
                        fontSize: "14px",
                      }}
                    >
                      <b style={{ display: "block", marginBottom: "4px" }}>
                        {msg.from === "bot" ? "🤖 Bot" : "🙋 You"}
                      </b>
                      {msg.text}
                    </div>
                  ))}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
  );
}

export default HistoryChat;
