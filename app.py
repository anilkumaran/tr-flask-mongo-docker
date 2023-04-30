from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

db_name = "SampleDotCom"
app = Flask(__name__)
app.config["MONGO_URI"] = f"mongodb://mongo:27017/{db_name}"
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
mongo = PyMongo(app)
db = mongo.db

@app.route("/")
def index():
    return jsonify(
        message="Welcome to sample.com"
    )

@app.route("/api/v1/users")
def get_all_users():
    users = db.users.find()
    data = []
    for user in users:
        item = {
            "id": str(user["_id"]),
            "name": user["Name"],
            "role": user["Role"]
        }
        data.append(item)
    return jsonify(
        data=data
    )

@app.route("/api/v1/users", methods=["POST"])
def create_user():
    data = request.get_json(force=True)
    db.users.insert_one({"Name": data["name"], "Role": data["role"]})
    return jsonify(
        message="User created successfully!"
    )

@app.route("/api/v1/users/<id>", methods=["DELETE"])
def delete_user(id):
    response = db.users.delete_one({"_id": ObjectId(id)})
    if response.deleted_count:
        message = f"User with id: {id} deleted successfully!"
    else:
        message = f"No User found with id {id}"
    return jsonify(
        message=message
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
