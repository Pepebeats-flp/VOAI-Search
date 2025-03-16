const express = require("express");
const axios = require("axios");
const Chat = require("../models/Chat");
require("dotenv").config(); // Cargar variables de entorno

const router = express.Router();

// Obtener todos los mensajes
router.get("/", async (req, res) => {
  try {
    const chats = await Chat.find().sort({ timestamp: 1 });
    res.json(chats);
  } catch (err) {
    res.status(500).json({ error: "Error al obtener los mensajes" });
  }
});

// Enviar un mensaje y recibir respuesta del bot
router.post("/", async (req, res) => {
  try {
    const { userMessage } = req.body;

    if (!userMessage) {
      return res.status(400).json({ error: "El mensaje del usuario es requerido." });
    }

    // 🔹 Guardar el mensaje del usuario en MongoDB
    const newChat = new Chat({ sender: "user", text: userMessage });
    await newChat.save();

    // 🔹 Enviar el mensaje al servidor Python
    const executionResponse = await axios.post("http://localhost:5002/execute", {
      code: userMessage // 🔹 Corrección: Se envía el mensaje correcto
    });

    // 🔹 Extraer correctamente la respuesta del bot
    const botResponse = executionResponse.data.bot_response;
    console.log("Bot response:", botResponse);
    if (!botResponse) {
      return res.status(500).json({ error: "No se recibió respuesta del código Python." });
    }

    // 🔹 Guardar la respuesta del bot en MongoDB
    const botChat = new Chat({ sender: "bot", text: botResponse });
    await botChat.save();

    res.json({ userMessage, botResponse });

  } catch (err) {
    console.error("Error en chat:", err);
    res.status(500).json({ error: "Hubo un problema procesando la consulta." });
  }
});


module.exports = router;
