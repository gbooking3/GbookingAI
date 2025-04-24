/* eslint-disable no-unused-vars */
import React from 'react';
import './Footer.css';
import { Link } from 'react-router-dom';

function Footer() {
  return (
    <footer className="site-footer">
      <div className="footer-content">
        <span>© {new Date().getFullYear()} Gbooking. All rights reserved.</span>
      </div>
      <div>
        <Link to="/contact" className="footer-link">Contact Us</Link>
      </div>
    </footer>
  );
}

export default Footer;
