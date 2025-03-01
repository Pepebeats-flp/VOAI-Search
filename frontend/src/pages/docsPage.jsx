// src/pages/DocsPage.jsx
import { Box, Typography, Paper } from "@mui/material";
import Header from "../components/header";

const DocsPage = () => {
  return (
    <Box sx={{ display: "flex", height: "100vh" }}>
      <Box sx={{ flexGrow: 1, display: "flex", flexDirection: "column" }}>
        <Header />
        <Paper sx={{ m: 2, p: 3 }}>
          <Typography variant="h4" gutterBottom>
            Documentación de VOAI-Search
          </Typography>
          <Typography variant="body1">
            Aquí puedes aprender cómo usar la plataforma para hacer consultas en los observatorios virtuales.
          </Typography>
        </Paper>
      </Box>
    </Box>
  );
};

export default DocsPage;
