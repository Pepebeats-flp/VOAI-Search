import { Box } from "@mui/material";
import { motion } from "framer-motion";
import deepseek from "../assets/deeplogo.jpg";
import gpt from "../assets/logogpt.jpg";

const AiIcon = ({ isDeepSeek, onToggle }) => {
  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        marginRight: "5px",
      }}
    >
      <motion.img
        src={isDeepSeek ? deepseek : gpt}
        alt="Chat Logo"
        onClick={onToggle}
        whileTap={{ scale: 0.9 }}
        transition={{ duration: 0.5 }}
        style={{
          width: "60px",
          height: "60px",
          objectFit: "cover",
          borderRadius: "50%",
          cursor: "pointer",
          paddingBottom: "5px",
        }}
      />
    </Box>
  );
};

export default AiIcon;
