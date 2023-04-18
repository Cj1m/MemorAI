import React, { useState } from "react";
import { Box, TextField, Button } from "@mui/material";

const ChatInput = ({ onSubmit }) => {
  const [message, setMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim()) {
      onSubmit(message);
      setMessage("");
    }
  };

  return (
    <Box
      component="form"
      display="flex"
      justifyContent="space-between"
      alignItems="center"
      onSubmit={handleSubmit}
    >
      <TextField
        label="Type your message"
        variant="outlined"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        fullWidth
        autoComplete="off"
      />
      <Button type="submit" variant="contained" color="primary">
        Send
      </Button>
    </Box>
  );
};

export default ChatInput;
