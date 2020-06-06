from flask import Flask, jsonify, request
from google.cloud import datastore

from schemas import JsonSchemaException, POST_VALIDATOR

datastore_client = datastore.Client()

app = Flask(__name__)


@app.route("/api/rate", methods=["POST"])
def rate():
    try:
        POST_VALIDATOR(request.json)
    except JsonSchemaException as e:
        return jsonify({"status": "error", "reason": f"invalid json format: {e}"}), 400

    return jsonify({"status": "success"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
