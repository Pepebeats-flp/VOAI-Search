const express = require("express");
const axios = require("axios");
const Chat = require("../models/Chat");

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

// Guardar un mensaje y hacer consulta TAP
router.post("/", async (req, res) => {
  try {
    const { userMessage } = req.body;

    // 🔹 Guardar el mensaje del usuario en MongoDB
    const newChat = new Chat({ role: "user", content: userMessage });
    await newChat.save();

    // 🔹 Enviar el mensaje a GPT para que genere el TAP URL y la consulta ADQL
    const gptResponse = await axios.post(
      "https://api.openai.com/v1/chat/completions",
      {
        model: "gpt-4o-mini",
        messages: [
          { role: "system", content: "Eres un asistente experto en astronomía y consultas TAP." },
          { role: "user", content: `Dado el mensaje: "${userMessage}", busca en la web y elige el mejor servicio TAP y genera la consulta ADQL correspondiente. Devuelve un JSON con 'tap_url' y 'query'` }
        ]
      },
      {
        headers: { Authorization: `Bearer TU_OPENAI_API_KEY` }
      }
    );

    const { tap_url, query } = JSON.parse(gptResponse.data.choices[0].message.content);

    // 🔹 Ejecutar la consulta en el servicio TAP usando Python
    const pyvoResponse = await axios.post("http://localhost:5002/query", {
      tap_url,
      query
    });

    const botResponse = JSON.stringify(pyvoResponse.data, null, 2);

    // 🔹 Guardar la respuesta en MongoDB
    const botChat = new Chat({ role: "bot", content: botResponse });
    await botChat.save();

    res.json({ userMessage, botResponse });

  } catch (err) {
    console.error("Error en chat:", err);
    res.status(500).json({ error: "Hubo un problema procesando la consulta." });
  }
});

module.exports = router;
