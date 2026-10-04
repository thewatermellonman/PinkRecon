from flask import Flask, request, jsonify, send_from_directory
from network_scan import scan_network
import os

FRONTEND_FOLDER = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "frontend"
    )
)

app = Flask(
    __name__,
    static_folder=FRONTEND_FOLDER
)

@app.route("/")
def index():
    return send_from_directory(
        FRONTEND_FOLDER,
        "index.html"
    )

@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory(
        FRONTEND_FOLDER,
        filename
    )

@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()

    network = data.get("network")

    if not network:
        return jsonify({
            "success": False,
            "error": "No network provided"
        }), 400

    try:
        results = scan_network(network)

        return jsonify({
            "success": True,
            "hosts": results
        })

    except Exception as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 500

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )