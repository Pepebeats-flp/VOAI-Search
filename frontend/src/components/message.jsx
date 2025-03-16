import { Box, Typography } from "@mui/material";

function Message({ text, sender }) {
  // Función para detectar si el texto es una URL
  const isLink = (text) => {
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    return text.match(urlRegex);
  };

  // Función para verificar si la URL es una imagen usando regex
  const isImageLink = (url) => {
    const imageRegex = /jpeg|jpg|gif|png/i;
    return url.match(imageRegex);
  }
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
        boxShadow: 3,
        "&:hover": {
          boxShadow: 5,
          transition: "0.2s ease-in-out",
        },
        wordBreak: "break-word", // Para que los enlaces largos no se salgan del contenedor
        overflowWrap: "break-word", // Para que el texto largo se divida correctamente
      }}
    >
      {isLink(text) ? (
        isImageLink(text) ? (
          <Box sx={{ textAlign: "center" }}>
            <img
              src={text}
              alt="Image"
              style={{
                maxWidth: "100%",
                maxHeight: "300px",
                objectFit: "contain",
                borderRadius: "8px",
              }}
            />
          </Box>
        ) : (
          <Typography variant="body2">
            <a
              href={text}
              target="_blank"
              rel="noopener noreferrer"
              style={{
                color: "inherit",
                textDecoration: "underline",
              }}
            >
              {text}
            </a>
          </Typography>
        )
      ) : (
        <Typography variant="body2">{text}</Typography>
      )}
    </Box>
  );
}

export default Message;
