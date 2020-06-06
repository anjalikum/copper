from flask import Flask, jsonify, request
from google.cloud import datastore
from google.cloud.datastore.helpers import GeoPoint

from schemas import JsonSchemaException, POST_VALIDATOR

datastore_client = datastore.Client()

app = Flask(__name__)


@app.route("/api/rate", methods=["POST"])
def rate():
    try:
        POST_VALIDATOR(request.json)
    except JsonSchemaException as e:
        return jsonify({"status": "error", "reason": f"invalid json format: {e}"}), 400

    key = datastore_client.key("Post")
    entity = datastore.Entity(key)
    entity.update({
        "department": request.json['department'],
        "badge": request.json['badge'],
        "comments": request.json['comments'],
        "location": GeoPoint(latitude=request.json['location'][0], longitude=request.json['location'][1]),
        "friendliness": request.json['ratings']['friendliness'],
        "difficulty": request.json['ratings']['difficulty'],
        "appropriateness": request.json['ratings']['appropriateness'],
        "helpfulness": request.json['ratings']['helpfulness'],
        "nonviolence": request.json['ratings']['nonviolence'],
        "race": request.json['tags']['race'],
        "gender": request.json['tags']['gender'],
        "age": request.json['tags']['age']
    })
    datastore_client.put(entity)

    return jsonify({"status": "success"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
