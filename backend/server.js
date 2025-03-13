require("dotenv").config();
const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const chatRoutes = require("./routes/chatRoutes");
const queryRoutes = require("./routes/queryRoutes");

const app = express();
app.use(express.json()); // Soporte para JSON
app.use(cors()); // Permitir solicitudes desde el frontend

// Conectar a MongoDB
mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => console.log("✅ Conectado a MongoDB"))
.catch(err => console.error("❌ Error al conectar MongoDB:", err));

// Rutas
app.use("/api/chats", chatRoutes);
app.use("/api/queries", queryRoutes);

const PORT = process.env.PORT || 5001;
app.listen(PORT, () => console.log(`🚀 Servidor corriendo en el puerto ${PORT}`));
