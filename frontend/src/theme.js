// src/theme.js
import { createTheme } from "@mui/material/styles";

const azul = "#112e41";
const azul_dark = "#0a1c2c"; // Más oscuro

const celeste = "#0962af";
const celeste_dark = "#06498a"; // Más oscuro

const naranjo = "#ff8008";
const naranjo_dark = "#cc6406"; // Ya definido correctamente

const marino = "#041017";
const marino_dark = "#020b0e"; // Más oscuro

const blanco = "#ffffff";
const blanco_dark = "#e0e0e0"; // Un tono gris claro como versión "oscura"

const negro = "#000000";
const negro_dark = "#000000"; // No tiene versión más oscura, sigue siendo negro puro

const theme = createTheme({
  palette: {
    azul: {
      main: azul,
      dark: azul_dark,
    },
    marino: {
      main: marino,
      dark: marino_dark,
    },
    celeste: {
      main: celeste,
      dark: celeste_dark,
    },
    naranjo: {
      main: naranjo,
      dark: naranjo_dark,
    },
    blanco: {
      main: blanco,
      dark: blanco_dark,
    },
    negro: {
      main: negro,
    }
  },
  typography: {
    fontFamily: "IBM Plex Mono, monospace",
    h1: { fontSize: "2.5rem", fontWeight: 700 }, // Título grande
    h2: { fontSize: "2rem", fontWeight: 600 }, // Subtítulo
    h3: { fontSize: "1.75rem", fontWeight: 500 },
    body1: { fontSize: "1rem" }, // Texto normal
    body2: { fontSize: "0.875rem" }, // Texto pequeño
    button: { fontSize: "1rem", textTransform: "none" }, // Tamaño de los botones
  },
});

export default theme;

