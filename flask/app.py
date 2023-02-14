from flask import Flask, render_template, request, url_for, redirect, jsonify
#from flask_pymongo import PyMongo
from pymongo import MongoClient

# Create a new Flask application and assigns it to the variable 'app'.
app = Flask(__name__)
# Create and execute mongodb
client = MongoClient(host="mongo", port=27017, username="root", password="pass", authSource="admin")
db = client["mongo"]
#db = client.flask_db
collection = db["people"]

@app.route("/")
def home():
    return render_template('index.html')

# The home page
@app.route("/hello")
def hello():
    return "Hello! v0.1.0"

@app.route("/person/<string:person_id>", methods=["GET"])
def get_person(person_id):
    person = collection.find_one({"id": person_id})
    if person:
        return jsonify(person), 200
    else:
        return jsonify({"error": "Person not found"}), 404

@app.route("/person", methods=["GET"])
def get_people():
    people = [person["id"] for person in collection.find()]
    return jsonify({"people": people}), 200

@app.route("/person/<string:person_id>", methods=["PUT"])
def update_person(person_id):
    person = request.get_json()
    person["id"] = person_id
    collection.replace_one({"id": person_id}, person, upsert=True)
    return jsonify({"message": "Person updated"}), 200

@app.route("/person/<string:person_id>", methods=["DELETE"])
def delete_person(person_id):
    result = collection.delete_one({"id": person_id})
    if result.deleted_count:
        return jsonify({"message": "Person deleted"}), 200
    else:
        return jsonify({"error": "Person not fount"}), 404

@app.route("/metrics")
def metrics():
    # Placeholder endpoint for monitoring
    return jsonify({}), 200

#@app.route('/person/<id>', methods=['POST'])
#def add_person(id):
    #person = request.form["person"]
    #data = request.get_json()
    # Do something with the data, like adding it to a database
    #return json.dumps({"status":"success"})

#@app.route('/person/<id>', methods=['PUT'])
#def update_person(id):

#@app.route('/person/<id>', methods=['DELETE'])
#def remove_person(id):

#@app.route('/person/<id>', methods=['GET'])
#def return_json(id):

#@app.route('/person/<id>', methods=['GET'])
#def get_json():

#@app.route('/person', methods=['GET'])
#def monitoring():

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)