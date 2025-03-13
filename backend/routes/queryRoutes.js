const express = require("express");
const Query = require("../models/Query");

const router = express.Router();

// Obtener todas las consultas
router.get("/", async (req, res) => {
  try {
    const queries = await Query.find().sort({ timestamp: -1 });
    res.json(queries);
  } catch (err) {
    res.status(500).json({ error: "Error al obtener las consultas" });
  }
});

// Guardar una consulta
router.post("/", async (req, res) => {
  try {
    const newQuery = new Query(req.body);
    await newQuery.save();
    res.status(201).json(newQuery);
  } catch (err) {
    res.status(500).json({ error: "Error al guardar la consulta" });
  }
});

module.exports = router;
