import { Box, TextField, IconButton } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import { useState } from "react";
import AiIcon from "../components/AiIcon";

function InputBox({ onSend, isDeepSeek, onToggle }) {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (text.trim()) {
      const iconValue = isDeepSeek ? "deepseek" : "openai";
      // Enviar un objeto con texto e ícono
      onSend({ text, aiIcon: iconValue });
      setText("");
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        p: 2,
        bgcolor: "azul.main",
        borderRadius: "8px",
        alignItems: "center",
      }}
    >
      <AiIcon isDeepSeek={isDeepSeek} onToggle={onToggle} />
      <TextField
        fullWidth
        variant="outlined"
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyUp={(e) => e.key === "Enter" && handleSend()}
        placeholder="¿Qué dato astronómico deseas obtener?"
        sx={{
          "& .MuiOutlinedInput-root": {
            "& fieldset": { borderColor: "blanco.main" },
            "&:hover fieldset": { borderColor: "blanco.main" },
            "&.Mui-focused fieldset": { borderColor: "blanco.main" },
          },
          input: { color: "blanco.main", typography: "body2" },
          "& .MuiInputBase-input::placeholder": { typography: "body2" },
        }}
      />
      <IconButton onClick={handleSend} disableRipple>
        <SendIcon
          sx={{
            marginLeft: "8px",
            color: "naranjo.main",
            "&:hover": {
              color: "naranjo.dark",
              transform: "scale(1.2)",
              transition: "0.2s ease-in-out",
            },
          }}
        />
      </IconButton>
    </Box>
  );
}

export default InputBox;
