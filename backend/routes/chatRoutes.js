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

router.post("/", async (req, res) => {
  try {
    const { userMessage } = req.body;

    if (!userMessage) {
      return res.status(400).json({ error: "El mensaje del usuario es requerido." });
    }

    // 🔹 Guardar el mensaje del usuario en MongoDB
    const newChat = new Chat({ sender: "user", text: userMessage });
    await newChat.save();

    // Verificar si la clave de OpenAI está disponible
    const openAiApiKey = process.env.OPENAI_API_KEY;
    if (!openAiApiKey) {
      return res.status(500).json({ error: "La clave de OpenAI no está configurada." });
    }

    // 🔹 Enviar el mensaje a GPT para generar código Python con PyVO
    const gptResponse = await axios.post(
      "https://api.openai.com/v1/chat/completions",
      {
        model: "gpt-4",
        messages: [
          {
            "role": "system",
            "content": "Eres un asistente experto en Astronomía y Observatorios Virtuales; genera código en Python con PyVO para acceder a datos de observatorios virtuales, identificando la base de datos adecuada, asegurando código listo para ejecutar sin errores, sin explicaciones fuera de comentarios, usando catálogos recomendados si la consulta es ambigua, aplicando solo métodos correctos de PyVO, descargando imágenes con .access_url y requests.get(), formateando correctamente con indentación de 4 espacios y retornando únicamente código en Python."
          },                    
          { role: "user", content: `Dado el mensaje: "${userMessage}", genera un script en Python usando PyVO para consultar el servicio apropiado.` }
        ]
      },
      {
        headers: { Authorization: `Bearer ${openAiApiKey}` }
      }
    );

    const pythonCode = gptResponse.data.choices[0]?.message?.content;

    if (!pythonCode) {
      return res.status(500).json({ error: "GPT no devolvió un código válido." });
    }

    // 🔹 Enviar el código a `query_service.py` para ejecutarlo
    const executionResponse = await axios.post("http://localhost:5002/execute", {
      code: pythonCode
    });

    console.log("Resultado de la ejecución de Python:", executionResponse.data); // DEBUG

    const botResponse = JSON.stringify(executionResponse.data, null, 2);

    if (!botResponse) {
      return res.status(500).json({ error: "No se recibió respuesta del código Python." });
    }

    // 🔹 Guardar la respuesta en MongoDB
    const botChat = new Chat({ sender: "bot", text: botResponse });
    await botChat.save();

    res.json({ userMessage, botResponse });

  } catch (err) {
    console.error("Error en chat:", err);
    res.status(500).json({ error: "Hubo un problema procesando la consulta." });
  }
});


module.exports = router;
