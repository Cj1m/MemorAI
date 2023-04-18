import React, { useState } from "react";
import { Box, Container, CssBaseline } from "@mui/material";
import ChatInput from "./components/ChatInput";
import ChatHistory from "./components/ChatHistory";

const App = () => {
  const [messages, setMessages] = useState([]);

  const handleSubmit = (message) => {
    setMessages([...messages, { role: "user", content: message }]);
    // Here, you would call your backend API to get the chatbot's response
    // and update the messages state with the chatbot's response.
  };

  return (
    <Container maxWidth="sm">
      <CssBaseline />
      <Box
        display="flex"
        flexDirection="column"
        minHeight="100vh"
        bgcolor="background.default"
        paddingTop={4}
        paddingBottom={4}
      >
        <ChatHistory messages={messages} />
        <ChatInput onSubmit={handleSubmit} />
      </Box>
    </Container>
  );
};

export default App;