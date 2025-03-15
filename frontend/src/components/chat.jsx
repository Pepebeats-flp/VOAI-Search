import { Box, Paper, Typography, TextField, IconButton, Menu } from "@mui/material";
import { useState, useEffect } from "react";
import InputBox from "./inputBox";
import Message from "./message";


const Chat = () => {
  const [messages, setMessages] = useState([]);

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

  // Función para enviar un mensaje al backend
  const sendMessage = async (text) => {
    // Agregar el mensaje del usuario al estado local
    setMessages((prev) => [...prev, { sender: "user", text }]);

    try {
      const response = await fetch("http://localhost:5001/api/chats", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userMessage: text }), // 🔹 Ahora enviamos 'userMessage'
      });

      if (!response.ok) throw new Error("Error al procesar el mensaje");

      const { botResponse } = await response.json(); // Recibimos la respuesta del bot

      // Agregar la respuesta del bot al estado local
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
          maxWidth: "800px", // Ajusta el ancho máximo del chat
          display: "flex", 
          flexDirection: "column",
          height: "80vh", // Ajusta la altura
          margin: "0 30px"// Ajusta el margen lateral
        }}
      >
      <Paper
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

          // 🎨 Personalización de la barra de scroll
          "&::-webkit-scrollbar": {
            width: "6px", // Ancho de la barra
          },
          "&::-webkit-scrollbar-thumb": {
            backgroundColor: "naranjo.main", // Color normal
            borderRadius: "20px",
          },
          "&::-webkit-scrollbar-thumb:hover": {
            // agrandar el tamaño del thumb
            backgroundColor: "naranjo.dark", // Color al pasar el mouse
          },
        }}
      >
        {/* Aquí se renderizarán los mensajes */}
        <Box sx={{ display: "flex", flexDirection: "column", gap: 1, p: 1 }}>
          {messages.map((msg, index) => (
              <Message key={index} text={msg.text} sender={msg.sender} />
            ))}      
        </Box>        

      </Paper>
        <InputBox onSend={sendMessage}/>
      </Box>
    </Box>
  );
};

export default Chat;
