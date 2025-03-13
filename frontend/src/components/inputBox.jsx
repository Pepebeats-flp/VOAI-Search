import { Box, TextField, IconButton } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import { useState } from "react";

function InputBox({ onSend }) {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (text.trim()) {
      onSend(text);
      setText("");
    }
  };

  return (
    <Box sx={{ display: "flex", p: 2, bgcolor: "azul.main", borderRadius: "8px" }}>
      <TextField
        fullWidth
        variant="outlined"
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyUp={(e) => e.key === "Enter" && handleSend()}
        placeholder="¿Qué dato astronómico deseas obtener?"
        sx={{
          "& .MuiOutlinedInput-root": {
            "& fieldset": {
              borderColor: "blanco.main", // Color del borde
            },
            "&:hover fieldset": {
              borderColor: "blanco.main", // Color del borde al pasar el mouse
            },
            "&.Mui-focused fieldset": {
              borderColor: "blanco.main", // Color del borde al estar enfocado
            },
          },
          input: {
            color: "blanco.main", // Color del texto
            typography: "body2",
          },
          placeholder: {
            color: "blanco.main", // Color del placeholder
          },
        "& .MuiInputBase-input::placeholder": {
        typography: "body2",
      }
        }} />
      <IconButton onClick={handleSend} disableRipple>
        <SendIcon sx={{
          marginLeft: "8px",
          color: "naranjo.main",
          "&:hover": {
            color: "naranjo.dark",
            transform: "scale(1.2)",
            transition: "0.2s ease-in-out",
          }
        }} />
      </IconButton>
    </Box>
  );
}

export default InputBox;

