import React, { useState } from "react";
import './AddUser.css'; // Importing the CSS file for styling

const API_URL = import.meta.env.VITE_API_URL;

function AddUser() {
  const [id, setID] = useState(0);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [ownid, setOwnID] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMessage(""); // Reset any previous error messages

    const newItem = { id, name, email, phone, ownid ,password};

    try {
      const response = await fetch(`${API_URL}/Gbooking`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newItem),
      });

      if (!response.ok) {
        throw new Error("Failed to add user");
      }

      alert("User added successfully!");
      setID(id + 1); // This is only needed if you need to increment the ID manually
      setName("");
      setEmail("");
      setPhone("");
      setOwnID("");
      setPassword("");
    } catch (error) {
      console.error("Error:", error);
      setErrorMessage("There was an issue adding the user. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit} className="form">
        <h2 className="form-title">Gbooking Register</h2>
        {errorMessage && <p className="error-message">{errorMessage}</p>}
        <div className="form-inputs">
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Full Name"
            required
            className="form-input"
          />
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
            required
            className="form-input"
          />
          <input
            type="tel"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            placeholder="Phone"
            required
            className="form-input"
          />
          <input
            type="text"
            value={ownid}
            onChange={(e) => setOwnID(e.target.value)}
            placeholder="Your ID"
            required
            className="form-input"
          />
               <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            required
            className="form-input"
          />
        </div>
        <button
          type="submit"
          className="form-button"
          disabled={loading}
        >
          {loading ? "Adding..." : "Add User"}
        </button>
      </form>
    </div>
  );
}

export default AddUser;
