/* eslint-disable react/prop-types */

import { ButtonGroup, Button, Box, Typography } from "@mui/material";

export default function ContactMethodSelector({ method, setMethod }) {
  return (
    <Box sx={{ width: '100%', mt: 2 }}>
      <Typography
        variant="subtitle2"
        sx={{ color: "#4B5563", mb: 1, fontWeight: 700 }}
      >
        Select how you want to receive your OTP
      </Typography>

      <ButtonGroup
        fullWidth
        variant="contained"
        sx={{
          boxShadow: "0px 1px 4px rgba(0, 0, 0, 0.2)",
          borderRadius: "8px",
          overflow: "hidden"
        }}
      >
        <Button
          onClick={() => setMethod("email")}
          sx={{
            flex: 1,
            bgcolor: method === "email" ? "#4ba6ca" : "#e0e0e0",
            color: method === "email" ? "#fff" : "#333",
            fontWeight: "bold",
            '&:hover': {
              bgcolor: method === "email" ? "primary.dark" : "#d5d5d5"
            }
          }}
        >
          EMAIL
        </Button>
        <Button
          onClick={() => setMethod("phone")}
          sx={{
            flex: 1,
            bgcolor: method === "phone" ? "#4ba6ca" : "#e0e0e0",
            color: method === "phone" ? "#fff" : "#333",
            fontWeight: "bold",
            '&:hover': {
              bgcolor: method === "phone" ? "#1E75DD" : "#d5d5d5"
            }
          }}
        >
          PHONE
        </Button>
      </ButtonGroup>
    </Box>
  );
}
