/* eslint-disable no-unused-vars */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import InputField from '../../../../components/input_field/InputField';
import useFormInput from '../../../../hooks/useFormInput';
import { REGEX, REGEX_MESSAGES } from '../../../../utils/consts';
import { apiPost } from '../../../../api/apiMethods';
import './ContactPage.css';

const ContactPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [feedbackMessage, setFeedbackMessage] = useState("");

  const nameInput = useFormInput('', REGEX.NAME, REGEX_MESSAGES.NAME);
  const emailInput = useFormInput('', REGEX.EMAIL, REGEX_MESSAGES.EMAIL);
  const messageInput = useFormInput('', /[\s\S]{10,}/, 'Message must be at least 10 characters');

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!nameInput.valid || !emailInput.valid || !messageInput.valid) {
      setFeedbackMessage("⚠️ Please fill out all fields correctly.");
      return;
    }

    const contactData = {
      name: nameInput.value,
      email: emailInput.value,
      message: messageInput.value
    };

    try {
      setLoading(true);
      setFeedbackMessage("");

      const response = await apiPost('contact/send-message', contactData);
      console.log("🧪 Full API response:", response);

      if (response?.message) {
        setFeedbackMessage("✅ Message sent successfully!");

        // Clear the form
        nameInput.setValue('');
        emailInput.setValue('');
        messageInput.setValue('');

        setTimeout(() => setFeedbackMessage(''), 4000);
      } else {
        setFeedbackMessage("❌ Failed to send message. Please try again.");
      }
    } catch (error) {
      console.error("❌ Submission error:", error);
      const errorMsg = error.response?.data?.error || "❌ Something went wrong. Please try again.";
      setFeedbackMessage(errorMsg);
      setTimeout(() => setFeedbackMessage(''), 4000);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="contact-container">
      <div className="contact-card">
        <h2 className="contact-title">📞 Contact Us</h2>
        <p className="contact-subtitle">We’d love to hear from you! Reach out with any questions or feedback.</p>

        <form className="contact-form" onSubmit={handleSubmit}>
          <InputField
            type="text"
            label="Your Name"
            value={nameInput.value}
            onChange={nameInput.handleChange}
            valid={nameInput.valid}
            focus={nameInput.handleFocus}
            blur={nameInput.handleBlur}
            instruction={nameInput.instruction}
          />

          <InputField
            type="email"
            label="Your Email"
            value={emailInput.value}
            onChange={emailInput.handleChange}
            valid={emailInput.valid}
            focus={emailInput.handleFocus}
            blur={emailInput.handleBlur}
            instruction={emailInput.instruction}
          />

          <InputField
            type="textarea"
            label="Your Message"
            value={messageInput.value}
            onChange={messageInput.handleChange}
            valid={messageInput.valid}
            focus={messageInput.handleFocus}
            blur={messageInput.handleBlur}
            instruction={messageInput.instruction}
            rows={8}
          />

          <button type="submit" disabled={loading}>
            {loading ? "Sending..." : "Send Message"}
          </button>
        </form>

        {feedbackMessage && (
          <div
            className="feedback-message"
            style={{
              marginTop: '20px',
              color: feedbackMessage.startsWith("✅") ? "green" : "red",
              fontWeight: "bold",
            }}
          >
            {feedbackMessage}
          </div>
        )}

        <button className="back-button" onClick={() => navigate('/')}>
          ⬅ Back to Home
        </button>
      </div>
    </div>
  );
};

export default ContactPage;
