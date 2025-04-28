/* eslint-disable no-unused-vars */
import { useState, useContext, useEffect } from "react";
import { User } from '../../context/UserContext';
import { apiPost } from '../../../../api/apiMethods';
import { ROUTE_PATHS, API_ENDPOINTS } from '../../../../utils/consts';
import { useLocation, useNavigate } from "react-router-dom";
import Cookies from "universal-cookie";

function ChatBot() {
  const navigateTo = useNavigate();
  const [messages, setMessages] = useState([
    { from: "bot", text: "Hello, I'm your secretary based in AI, a crafty place for booking appointments. How can I help?" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [conversationId, setConversationId] = useState(null);

  const userContext = useContext(User);
  const user = userContext?.auth?.userDetails || {};
  const location = useLocation();

  // ✅ Redirect to login if no access token AND user is on /dashboard
  useEffect(() => {
    const cookies = new Cookies();
    const accessToken = cookies.get("access_token");

    const isOnDashboard = location.pathname === ROUTE_PATHS.MAIN.DASHBOARD;

    if (!accessToken && isOnDashboard) {
      userContext.setAuth(null); // Clear any existing user context
      navigateTo(ROUTE_PATHS.AUTH.LOGIN, {
        state: { logged_out: false },
        replace: true,
      });
    }
  }, [location.pathname, navigateTo, userContext]);

  // Typing effect function that updates the message in place
  const typeMessage = (message, delay = 100) => {
    return new Promise((resolve) => {
      let currentMessage = "";
      let index = 0;

      const interval = setInterval(() => {
        currentMessage += message[index];
        setMessages((prev) => {
          const newMessages = [...prev];
          newMessages[newMessages.length - 1] = { from: "bot", text: currentMessage };
          return newMessages;
        });
        index++;

        if (index === message.length) {
          clearInterval(interval);
          resolve();
        }
      }, delay);
    });
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { from: "user", text: input.trim() };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setErrorMessage("");
    setLoading(true);

    const messageData = {
      id: user.ownid,
      name: user.name,
      message: userMessage.text,
      conversation_id: conversationId, // include existing conversation ID if any
    };

    try {
      const response = await apiPost(API_ENDPOINTS.MAIN.CHAT_MESSAGE, messageData);

      // Add the bot's response and start typing effect
      setMessages((prev) => [...prev, { from: "bot", text: "" }]); // Add placeholder for bot message
      await typeMessage(response.message, 50); // Adjust the delay as needed

      // Store conversation ID if it's the first message
      if (response.conversation_id && !conversationId) {
        setConversationId(response.conversation_id);
      }
    } catch (error) {
      setErrorMessage("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleLogoutClick = () => {
    const cookies = new Cookies();
    cookies.remove("access_token", { path: "/" });
    cookies.remove("refresh_token", { path: "/" });

    // Also optionally clear context
    userContext.setAuth(null);

    navigateTo(ROUTE_PATHS.AUTH.LOGIN, {
      state: { logged_out: true },
      replace: true,
    });
  };

  const handleProfileClick = () => navigateTo(ROUTE_PATHS.MAIN.PROFILE);
  const handleDashboardClick = () => navigateTo(ROUTE_PATHS.MAIN.DASHBOARD);
  const handleHistoryClick = () => navigateTo(ROUTE_PATHS.MAIN.HISTORY);

  return (
    <div style={{ display: "flex", minHeight: "100vh", position: "relative" }}>
      {/* Sidebar */}
      <div
        style={{
          width: "200px",
          backgroundColor: "#0d47a1",
          color: "#fff",
          padding: "20px",
          display: "flex",
          flexDirection: "column",
          fontSize: "16px",
          position: "absolute",
          top: 0,
          left: isSidebarOpen ? "0" : "-220px",
          height: "100%",
          transition: "left 0.3s ease-in-out",
          zIndex: 10,
        }}
      >
        <h3 style={{ marginBottom: "20px" }}>☰ Menu</h3>

        <div style={{ marginBottom: "10px" }}>
          <div onClick={handleDashboardClick} style={{ cursor: "pointer" }}>
            📊 Dashboard
          </div>
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              marginTop: "10px",
              marginLeft: "20px",
              gap: "10px",
            }}
          >
            <div onClick={handleProfileClick} style={{ cursor: "pointer" }}>
              👤 Profile
            </div>
            <div onClick={handleLogoutClick} style={{ cursor: "pointer" }}>
              🔓 Logout
            </div>
            <div onClick={handleHistoryClick} style={{ cursor: "pointer" }}>
              🕓 History
            </div>
          </div>
        </div>
      </div>

      {/* Toggle Sidebar Button */}
      <button
        onClick={() => setIsSidebarOpen(!isSidebarOpen)}
        style={{
          position: "absolute",
          top: "20px",
          left: "20px",
          zIndex: 20,
          background: "#0d47a1",
          color: "#fff",
          border: "none",
          padding: "10px 14px",
          borderRadius: "6px",
          cursor: "pointer",
        }}
      >
        ☰ List
      </button>

      {/* Chat area */}
      <div className="form-container" style={{ flex: 1, padding: "40px", marginLeft: "0px" }}>
        <div className="form">
          <h2 className="form-title">Gbooking ChatBot</h2>

          {/* User Profile Card */}
          <div
            style={{
              backgroundColor: "#e3f2fd",
              padding: "12px 16px",
              borderRadius: "10px",
              marginBottom: "16px",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              fontSize: "14px",
              color: "#333",
              boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
            }}
          >
            <div>
              <b>{user.name || "No Name"}</b>
              <br />
            </div>
            <span style={{ fontSize: "24px" }}>👤</span>
          </div>

          {/* Chat messages */}
          <div
            style={{
              flex: 1,
              height: "300px",
              overflowY: "auto",
              padding: "10px",
              border: "1px solid #ccc",
              borderRadius: "10px",
              marginBottom: "16px",
              backgroundColor: "#f9f9f9",
            }}
          >
            {messages.map((msg, idx) => (
              <div
                key={idx}
                style={{
                  margin: "6px 0",
                  padding: "10px 14px",
                  borderRadius: "16px",
                  backgroundColor: msg.from === "user" ? "#d0ebff" : "#eaeaea",
                  textAlign: msg.from === "user" ? "right" : "left",
                  alignSelf: msg.from === "user" ? "flex-end" : "flex-start",
                  maxWidth: "80%",
                  marginLeft: msg.from === "user" ? "auto" : "0",
                  marginRight: msg.from === "bot" ? "auto" : "0",
                  whiteSpace: "pre-wrap",
                  direction: "ltr",
                }}
              >
                {msg.text}
              </div>
            ))}
          </div>

          {errorMessage && <p className="error-message">{errorMessage}</p>}

          {/* Input box */}
          <form onSubmit={handleSend} className="form-inputs" style={{ display: "flex", gap: "8px" }}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="form-input"
              required
            />
            <button type="submit" className="form-button" disabled={loading}>
              {loading ? "Sending..." : "Send"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default ChatBot;
