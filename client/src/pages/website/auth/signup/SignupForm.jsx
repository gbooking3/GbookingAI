import  { useState } from "react";
import './SignupPage.css';
import { apiPost } from '../../../../api/apiMethods';

const API_URL = import.meta.env.VITE_API_URL;

function SignupForm() {
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

    const newItem = {  name, email, phone, ownid };

    try {
      const response = await apiPost('auth/signup',  newItem)
      alert("User added successfully!");
      setName("");
      setEmail("");
      setPhone("");
      setOwnID("");
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

export default SignupForm;