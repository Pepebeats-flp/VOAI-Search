import { AppBar, Toolbar, Typography, Button, Box } from "@mui/material";
import { Link } from "react-router-dom";
import logo from "../assets/logo.png";

const Header = () => {
  return (
    <AppBar position="static" sx={{ backgroundColor: "marino.main", padding: "0.5rem", marginBottom: "30px" }}>
      <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
        {/* Logo con enlace al chat */}
        <Box component={Link} to="/" sx={{ display: "flex", alignItems: "center", textDecoration: "none" }}>
          <img src={logo} alt="Logo" style={{ height: 70 }} />
        </Box>

        {/* Contenedor para los links alineados a la derecha */}
        <Box sx={{ display: "flex", gap: 2 }}>
          <Button component={Link} to="/chat" variant="contained" sx={{ backgroundColor: "naranjo.main", color: "blanco.main", "&:hover": { backgroundColor: "naranjo.dark" } }}>
            Docs
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
