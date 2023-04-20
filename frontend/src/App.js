import React, { useState } from "react";
import { Grid, Container, CssBaseline } from "@mui/material";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import ChatInput from "./components/ChatInput";
import ChatHistory from "./components/ChatHistory";
import ChatToolbar from "./components/ChatToolbar";

const theme = createTheme({
  palette: {
    mode: "dark",
  },
});


const App = () => {
  const [messages, setMessages] = useState([]);
  const [isWaitingForResponse, setIsWaitingForResponse] = useState(false);
  const [currentInstance, setCurrentInstance] = useState("");

  const handleSubmit = async (message) => {
    setMessages((prevMessages) => [...prevMessages, { role: "user", content: message }]);
    setIsWaitingForResponse(true);

    try {
      const response = await fetch('/interact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
      });
      const data = await response.json();
      setMessages((prevMessages) => [...prevMessages, { role: "MemorAI", content: data.response }]);
    } catch (error) {
      console.error('Error communicating with the backend API:', error);
    } finally {
      setIsWaitingForResponse(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <ChatToolbar currentInstance={currentInstance} setCurrentInstance={setCurrentInstance} />
      <Container maxWidth="md">
        <Grid container direction="column" minHeight="calc(100vh - 64px)" spacing={2} paddingTop={4} paddingBottom={2}>
          <ChatHistory messages={messages} />
          <ChatInput onSubmit={handleSubmit} isWaitingForResponse={isWaitingForResponse} />
        </Grid>
      </Container>
    </ThemeProvider>
  );
};

export default App;