/* eslint-disable no-unused-vars */
import React from 'react';
import { useNavigate } from 'react-router-dom'; // ⬅️ Add this line
import './ContactPage.css'; // Optional if you're using plain CSS

const ContactPage = () => {
  const navigate = useNavigate(); // ⬅️ Hook to navigate

  return (
    <div className="contact-container">
      <div className="contact-card">
        <h2 className="contact-title">📞 Contact Us</h2>
        <p className="contact-subtitle">We’d love to hear from you! Reach out with any questions or feedback.</p>

        <form className="contact-form">
          <input type="text" placeholder="Your Name" required />
          <input type="email" placeholder="Your Email" required />
          <textarea placeholder="Your Message" rows="5" required></textarea>
          <button type="submit">Send Message</button>
        </form>

        <button 
          className="back-button" 
          onClick={() => navigate('/')}
        >
          ⬅ Back to Home
        </button>
      </div>
    </div>
  );
};

export default ContactPage;
