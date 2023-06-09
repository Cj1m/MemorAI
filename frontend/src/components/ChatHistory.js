import React from "react";
import { Box, Paper } from "@mui/material";
import ChatMessage from "./ChatMessage";

const ChatHistory = ({ messages }) => {
  return (
    <Box
      display="flex"
      flexDirection="column"
      overflow="auto"
      flexGrow={1}
      component={Paper}
      p={2}
      paddingBottom={2}
    >
      {messages.map((message, index) => (
        <ChatMessage key={index} message={message.content} sender={message.role} />
      ))}
    </Box>
  );
};

export default ChatHistory;