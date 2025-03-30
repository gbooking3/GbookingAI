import React, { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL;

function AddUser() {
  const [id, setID] = useState(0);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [ownid, setOwnID] = useState("");

  console.log("API URL:", API_URL);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const newItem = { id, name, email, phone, ownid };

    const response = await fetch(`${API_URL}/Gbooking`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newItem),
    });

    if (response.ok) {
      console.log("User added successfully!");
      alert("User added successfully");

      setID(id + 1);
      setName("");
      setEmail("");
      setPhone("");
      setOwnID("");
    } else {
      console.error("Failed to add user");
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gradient-to-r from-cyan-500 to-white">
      <form onSubmit={handleSubmit} className="bg-white shadow-xl rounded-2xl p-8 w-full max-w-md space-y-6 border border-cyan-500">
        <h2 className="text-2xl font-bold text-cyan-600 text-center">Add User</h2>
        <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" required className="w-full p-3 border border-cyan-400 rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500" />
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required className="w-full p-3 border border-cyan-400 rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500" />
        <input type="tel" value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="Phone" required className="w-full p-3 border border-cyan-400 rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500" />
        <input type="text" value={ownid} onChange={(e) => setOwnID(e.target.value)} placeholder="Own ID" required className="w-full p-3 border border-cyan-400 rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500" />
        <button type="submit" className="w-full p-3 bg-cyan-600 text-white rounded-md hover:bg-cyan-700 transition shadow-md">Add User</button>
      </form>
    </div>
  );
}

export default AddUser;
