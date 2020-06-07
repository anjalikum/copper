from flask import Flask, jsonify, request
from google.cloud import datastore
from google.cloud.datastore.helpers import GeoPoint

from schemas import JsonSchemaException, POST_VALIDATOR

datastore_client = datastore.Client()

app = Flask(__name__)


@app.route("/api/ratings", methods=["GET", "POST"])
def rate():
    if request.method == "GET":
        if request.args.get("department") is None:
            return jsonify({"status": "error", "reason": "query parameter 'department' is required"}), 400

        query = datastore_client.query(kind="Post")
        query.add_filter("department", "=", request.args.get("department"))

        entities = [entity for entity in query.fetch()]
        return jsonify({"status": "success", "data": entities})

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


@app.route("/api/departments/<string:state>")
def departments_for_state(state):
    state = state.upper()
    if len(state) != 2:
        return jsonify({"status": "error", "reason": "state code must be two characters long"}), 400

    query = datastore_client.query(kind="Department")
    query.add_filter("state_code", "=", state)

    entities = [entity for entity in query.fetch()]
    return jsonify({"status": "success", "data": entities})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
