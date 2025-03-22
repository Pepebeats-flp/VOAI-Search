const mongoose = require("mongoose");

const ChatSchema = new mongoose.Schema({
  text: { type: String, required: true },
  sender: { type: String, required: true },
  timestamp: { type: Date, default: Date.now },
  aiIcon: { type: String, required: false }
});

module.exports = mongoose.model("Chat", ChatSchema);
