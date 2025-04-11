import { useState, useContext } from "react";
import { User } from '../../context/UserContext';
import { useNavigate } from 'react-router-dom';

function ChatBot() {
  const navigate = useNavigate();
  const [messages, setMessages] = useState([
    { from: "bot", text: "👋 Hi! How can I help you today" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [isSidebarOpen, setIsSidebarOpen] = useState(false); // sidebar toggle

  const userContext = useContext(User);
  const user = userContext?.auth?.userDetails || {};

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { from: "user", text: input.trim() };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setErrorMessage("");
    setLoading(true);

    try {
      setTimeout(() => {
        const botMessage = {
          from: "bot",
          text: `🤖 You said: "${userMessage.text}". Let me know if you need anything else.`
        };
        setMessages((prev) => [...prev, botMessage]);
        setLoading(false);
      }, 700);
    } catch (error) {
      setErrorMessage("Something went wrong. Please try again.");
      setLoading(false);
    }
  };

  const handleLogoutClick = () => navigate("/login");
  const handleProfileClick = () => navigate("/profile");
  const handleDashboardClick = () => navigate("/dashboard");

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
          gap: "20px",
          fontSize: "16px",
          position: "absolute",
          top: 0,
          left: isSidebarOpen ? "0" : "-220px",
          height: "100%",
          transition: "left 0.3s ease-in-out",
          zIndex: 10,
        }}
      >
        <h3>☰ Menu</h3>
        <div onClick={handleDashboardClick} style={{ cursor: "pointer" }}>📊 Dashboard</div>
        <div onClick={handleProfileClick} style={{ cursor: "pointer" }}>👤 Profile</div>
        <div onClick={handleLogoutClick} style={{ cursor: "pointer" }}>🔓 Logout</div>
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
          cursor: "pointer"
        }}
      >
        ☰ List
      </button>

      {/* Chat area */}
      <div className="form-container" style={{ flex: 1, padding: "40px", marginLeft: "0px" }}>
        <div className="form">
          <h2 className="form-title">Gbooking ChatBot</h2>

          {/* User Profile Card */}
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
              <b>{user.name || "No Name"}</b><br />
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
