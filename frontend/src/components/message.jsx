import { Box, Typography } from "@mui/material";

function Message({ text, sender }) {
  return (
    <Box
      sx={{
        bgcolor: sender === "user" ? "naranjo.main" : "blanco.main",
        color: sender === "user" ? "blanco.main" : "marino.main",
        p: 1,
        my: 1,
        borderRadius: 1,
        maxWidth: "80%",
        alignSelf: sender === "user" ? "flex-end" : "flex-start",
        //sombras blancas
        boxShadow: 3,
        "&:hover": {
          boxShadow: 5,
          transition: "0.2s ease-in-out",
        },
      }}
    >
      <Typography variant="body2">{text}</Typography>
    </Box>
  );
}

export default Message;
