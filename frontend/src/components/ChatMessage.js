import React from "react";
import { Typography, Box } from "@mui/material";

const ChatMessage = ({ message, sender }) => {
  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems={sender === "user" ? "flex-end" : "flex-start"}
      marginBottom={2}
    >
      <Typography variant="body1">{message}</Typography>
    </Box>
  );
};

export default ChatMessage;