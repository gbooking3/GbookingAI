import { useState } from "react";

function ChatBot() {
  const [messages, setMessages] = useState([
    { from: "bot", text: "👋 Hi! How can I help you today?" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { from: "user", text: input.trim() };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setErrorMessage("");
    setLoading(true);

    try {
      // Simulate bot reply
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

  return (
    <div className="form-container">
      <div className="form">
        <h2 className="form-title">Gbooking ChatBot</h2>

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
  );
}

export default ChatBot;
