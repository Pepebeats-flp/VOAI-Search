const mongoose = require("mongoose");

const QuerySchema = new mongoose.Schema({
  user: { type: String, required: true },
  queryText: { type: String, required: true },
  response: { type: String, required: true },
  timestamp: { type: Date, default: Date.now }
});

module.exports = mongoose.model("Query", QuerySchema);
