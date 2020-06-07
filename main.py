from flask import Flask, jsonify, request
from google.cloud import datastore
from google.cloud.datastore.helpers import GeoPoint

from schemas import JsonSchemaException, POST_VALIDATOR

datastore_client = datastore.Client()

app = Flask(__name__)


@app.route("/api/ratings", methods=["GET", "POST"])
def rate():
    # Handle get method
    if request.method == "GET":
        # Ensure department parameter exists
        if request.args.get("department") is None:
            return jsonify({"status": "error", "reason": "query parameter 'department' is required"}), 400

        # Construct query for all posts with matching department
        query = datastore_client.query(kind="Post")
        query.add_filter("department", "=", request.args.get("department"))

        # Retrieve all posts
        entities = [entity for entity in query.fetch()]
        return jsonify({"status": "success", "data": entities})

    # Validate request body by schema in `./schemas/post.json`
    try:
        POST_VALIDATOR(request.json)
    except JsonSchemaException as e:
        return jsonify({"status": "error", "reason": f"invalid json format: {e}"}), 400

    # Create key and associated entity
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

    # Insert into datastore
    datastore_client.put(entity)

    return jsonify({"status": "success"})


@app.route("/api/departments/<string:state>")
def departments_for_state(state):
    # Ensure state code is consistent with those in datastore
    state = state.upper()
    if len(state) != 2:
        return jsonify({"status": "error", "reason": "state code must be two characters long"}), 400

    # Construct query for all departments with matching state abbreviation
    query = datastore_client.query(kind="Department")
    query.add_filter("state_code", "=", state)

    # Retrieve all departments
    entities = [entity for entity in query.fetch()]
    return jsonify({"status": "success", "data": entities})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
