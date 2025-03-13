from flask import Flask, request, jsonify
from pyvo.dal import tap

app = Flask(__name__)

@app.route("/query", methods=["POST"])
def execute_query():
    data = request.json
    tap_url = data.get("tap_url")  # 🔹 Ahora recibimos el TAP URL
    query = data.get("query")

    if not tap_url or not query:
        return jsonify({"error": "Faltan datos para ejecutar la consulta"}), 400

    try:
        # 🔹 Usamos el TAP URL que envió GPT
        service = tap.TAPService(tap_url)
        result = service.search(query)
        result_table = result.to_table().to_pandas()

        return jsonify(result_table.to_dict(orient="records"))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5002, debug=True)
