// src/pages/ChatPage.jsx
import { Box } from "@mui/material";
import Header from "../components/header";
import Chat from "../components/chat";

const ChatPage = () => {
  return (
    <Box sx={{ display: "flex", height: "100vh", backgroundColor: "azul.main" }}>
      <Box sx={{ flexGrow: 1, display: "flex", flexDirection: "column" }}>
        <Header />
        <Chat />
      </Box>
    </Box>
  );
};

export default ChatPage;
