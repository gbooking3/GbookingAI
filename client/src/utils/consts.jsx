
export const API_ENDPOINTS = {
    AUTH: {
      LOGIN       : "auth/login",
      LOGOUT      : "auth/logout",
      SIGNUP      : "auth/signup",
      VERIFY_OTP  : "auth/verify-otp",
      RESEND_OTP  : "auth/resend-otp",
      REFRESH     : "auth/refresh-token"
    },
    MAIN: {}
  };
  


  
// Just for App.js file
export const ROUTE_PATHS = {
    AUTH: {
      LOGIN  : "/login",
      SIGNUP : "/signup",
      OTP    : "/otp"
    },
    MAIN: {
      HOME      : "/",
      DASHBOARD : "/dashboard",
      PROFILE   : "/profile"
    }
  };
  
  
export const ERROR_CODES = {};

export const REGEX = {
    ID    : /^\d{9}$/,                                          // Israeli ID: 9 digits, optionally padded with zeros (common format)
    NAME  : /^[A-Za-z ]{3,23}$/,                                 // Name: English letters only (3 to 23 characters)
    EMAIL : /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/,  // Email: Common pattern
    PHONE : /^(?:\+972-?|0)?5[0-9]{8}$/                         // Israeli Phone: supports 05X-XXXXXXX, +9725XXXXXXXX, or 05XXXXXXXX
};

export const REGEX_MESSAGES = {
  ID: "ID must be exactly 9 digits (numbers only). No spaces or letters allowed.",
  NAME: "Name should be 3 to 23 characters long. Only English letters and spaces are allowed.",
  EMAIL: "Please enter a valid email address (e.g. name@example.com).",
  PHONE: "Phone number must be a valid Israeli mobile format (e.g. 0501234567 or +972501234567)."
};

  