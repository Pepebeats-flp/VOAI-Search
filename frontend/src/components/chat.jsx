import { Box, Paper, Typography, TextField, IconButton, Menu } from "@mui/material";
import { useState } from "react";
import InputBox from "./inputBox";
import Message from "./message";

const Chat = () => {
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
          <Message text="Hola" sender="user"/>  
          <Message text="Hola, ¿cómo estás?" sender="other"/>
          <Message text="Bien, gracias" sender="user"/>
          <Message text="¿Y tú?" sender="user"/>
          <Message text="También bien" sender="other"/>
          <Message text="¿Qué has hecho hoy?" sender="user"/>
          <Message text="He estado trabajando" sender="other"/>
          <Message text="¿Y tú?" sender="other"/>
          <Message text="He estado programando" sender="user"/>
          <Message text="¿Qué has programado?" sender="user"/>
          <Message text="Un chat" sender="other"/>
          <Message text="¿Y tú?" sender="other"/>
          <Message text="Un chat" sender="user"/>
          <Message text="¿Qué lenguaje?" sender="user"/>
          <Message text="JavaScript" sender="other"/>
          <Message text="¿Y tú?" sender="other"/>
          <Message text="JavaScript" sender="user"/>
          <Message text="¿Qué framework?" sender="user"/>
          <Message text="React" sender="other"/>
          <Message text="¿Y tú?" sender="other"/>              
        </Box>        

      </Paper>
        <InputBox/>
      </Box>
    </Box>
  );
};

export default Chat;
