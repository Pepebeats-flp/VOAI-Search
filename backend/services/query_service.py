import subprocess
import tempfile
import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

def limpiar_codigo(python_code):
    """Elimina los delimitadores Markdown y descarta texto fuera del bloque de código."""
    lines = python_code.split("\n")
    clean_lines = []
    in_code_block = False
    
    for line in lines:
        if line.strip().startswith("```python"):
            in_code_block = True
            continue
        elif line.strip().startswith("```"):
            in_code_block = False
            continue
        if in_code_block or line.strip():  # Agregar solo líneas de código
            clean_lines.append(line)

    return "\n".join(clean_lines).strip()

@app.route("/execute", methods=["POST"])
def execute_code():
    try:
        data = request.get_json()
        python_code = data.get("code")

        if not python_code:
            return jsonify({"error": "No se recibió código para ejecutar."}), 400

        # Limpiar el código antes de ejecutarlo
        python_code = limpiar_codigo(python_code)

        # Crear un archivo temporal con el código
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
            temp_file.write(python_code.encode("utf-8"))
            temp_file_path = temp_file.name

        # Ejecutar el archivo en un subproceso
        try:
            result = subprocess.run(["python3", temp_file_path], capture_output=True, text=True, timeout=30)
            output = result.stdout if result.stdout else result.stderr
        except subprocess.TimeoutExpired:
            output = "Error: El código tardó demasiado en ejecutarse."
        except Exception as e:
            output = f"Error al ejecutar el código: {str(e)}"
        finally:
            os.remove(temp_file_path)

        return jsonify({"code_executed": python_code, "output": output})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
