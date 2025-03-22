import { useState } from "react";
import InputBox from "./inputBox";

function ParentComponent() {
  // Estado para controlar cuál ícono se muestra (true: deepseek, false: gpt)
  const [isDeepSeek, setIsDeepSeek] = useState(true);

  const handleToggleAiIcon = () => {
    setIsDeepSeek((prev) => !prev);
  };

  const handleSendMessage = ({ text, aiIcon }) => {
    console.log("Mensaje:", text);
    console.log("Ícono seleccionado:", aiIcon);
  };

  return (
    <div>
      <InputBox
        onSend={handleSendMessage}
        isDeepSeek={isDeepSeek}
        onToggle={handleToggleAiIcon}
      />
    </div>
  );
}

export default ParentComponent;
