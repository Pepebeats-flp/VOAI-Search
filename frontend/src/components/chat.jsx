import { Box, Paper } from "@mui/material";
import { useState, useEffect, useRef } from "react";
import InputBox from "./inputBox";
import Message from "./Message";

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [shouldScroll, setShouldScroll] = useState(true);
  const messagesEndRef = useRef(null);
  const containerRef = useRef(null);
  // Supongamos que Chat también maneja el estado del ícono:
  const [isDeepSeek, setIsDeepSeek] = useState(true);

  // Cargar mensajes desde la API
  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const response = await fetch("http://localhost:5001/api/chats");
        if (!response.ok) throw new Error("Error al obtener mensajes");
        const data = await response.json();
        setMessages(data);
      } catch (error) {
        console.error("Error cargando mensajes:", error);
      }
    };

    fetchMessages();
    const interval = setInterval(fetchMessages, 2000);
    return () => clearInterval(interval);
  }, []);

  // Manejar el scroll del contenedor
  useEffect(() => {
    const container = containerRef.current;
    const handleScroll = () => {
      if (container.scrollTop + container.clientHeight >= container.scrollHeight - 50) {
        setShouldScroll(true);
      } else {
        setShouldScroll(false);
      }
    };

    container.addEventListener("scroll", handleScroll);
    return () => container.removeEventListener("scroll", handleScroll);
  }, []);

  // Auto-scroll condicional al final del chat
  useEffect(() => {
    if (shouldScroll) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, shouldScroll]);

  // Función para alternar el ícono (que se pasa a InputBox)
  const handleToggleAiIcon = () => {
    setIsDeepSeek((prev) => !prev);
  };

  // Función para enviar un mensaje al backend con texto e ícono
  const sendMessage = async ({ text, aiIcon }) => {
    // Agregar el mensaje del usuario al estado, opcionalmente incluyendo el dato del ícono
    setMessages((prev) => [...prev, { sender: "user", text, aiIcon }]);
    try {
      const response = await fetch("http://localhost:5001/api/chats", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        // Enviar ambos datos en la solicitud
        body: JSON.stringify({ userMessage: text, aiIcon }),
      });
      if (!response.ok) throw new Error("Error al procesar el mensaje");
      const { botResponse } = await response.json();
      setMessages((prev) => [...prev, { sender: "bot", text: botResponse }]);
    } catch (error) {
      console.error("Error enviando mensaje:", error);
    }
  };

  return (
    <Box 
      sx={{ 
        display: "flex", 
        justifyContent: "center", 
        alignItems: "center", 
        height: "100vh",
        backgroundColor: "azul.main"
      }}
    >
      <Box 
        sx={{ 
          width: "100%", 
          maxWidth: "800px",
          display: "flex", 
          flexDirection: "column",
          height: "80vh",
          margin: "0 30px"
        }}
      >
        <Paper
          ref={containerRef}
          elevation={3}
          sx={{
            p: 2,
            flexGrow: 1,
            overflowY: "auto",
            backgroundColor: "marino.main",
            borderRadius: "20px",
            maxWidth: "730px",
            marginLeft: "15px",
            marginRight: "30px",
            "&::-webkit-scrollbar": {
              width: "6px",
            },
            "&::-webkit-scrollbar-thumb": {
              backgroundColor: "naranjo.main",
              borderRadius: "20px",
            },
            "&::-webkit-scrollbar-thumb:hover": {
              backgroundColor: "naranjo.dark",
            },
          }}
        >
          <Box sx={{ display: "flex", flexDirection: "column", gap: 1, p: 1 }}>
            {messages.map((msg, index) => (
              <Message key={index} text={msg.text} sender={msg.sender} />
            ))}
            {/* Elemento para marcar el final de los mensajes */}
            <div ref={messagesEndRef} />
          </Box>        
        </Paper>
        <InputBox
          onSend={sendMessage}
          isDeepSeek={isDeepSeek}
          onToggle={handleToggleAiIcon}
        />
      </Box>
    </Box>
  );
};

export default Chat;
