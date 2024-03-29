from flask import Flask, render_template, request, url_for, redirect, jsonify, Response
import pymongo
from pymongo import MongoClient
import bson
from bson.objectid import ObjectId
from bson import ObjectId

# Create a new Flask application and assigns it to the variable 'app'.
app = Flask(__name__)
# Create and execute mongodb
def get_db():
    client = MongoClient(host="mongo",
                        port=27017,
                        username="root",
                        password="pass",
                        authSource="admin")
    # Connect to data base then to collection (/myMongo/people)
    db = client["mongo"]
    db["myPeople"].create_index("person_id", unique=True)
    return db

# Home page.
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/metrics")
def hello():
    return "Hello! v0.1.0"

@app.route("/person/", methods=["GET"])
def get_person():
    person_id = request.args.get("person_id")
    if not person_id:
        return jsonify({"error": "Person ID not provided."}), 400
    db = get_db()
    people = db["myPeople"]
    person = people.find_one({"person_id": person_id})
    if person:
        person["person_id"] = str(person["person_id"])
        return jsonify(person), 200
    else:
        return jsonify({"error": "Person not found."}), 404


# To get the all peoples in data base.
@app.route("/person", methods=["GET"])
def get_peoples():
    try:
        db = get_db()
        people = db["myPeople"]
        _peoples = people.find()
        peoples = [{
	    "person_id": person["person_id"],
            #"person_id": str(person["_id"]),
            "name": person["name"],
            "age": person["age"],
            "gender": person["gender"],
            "phone": person["phone"]
            } for person in _peoples]
        return jsonify({"peoples": peoples})
    except Exception as e:
        return jsonify({"error": f"Error while fetching persons: {str(e)}"}), 500
    finally:
        if type(db) == MongoClient:
            db.close()

# Create some person.
@app.route("/person", methods=["POST"])
def create_person():
    db = get_db()
    people = db["myPeople"]
    person_id = request.form.get("person_id")
    name = request.form.get("name")
    age = request.form.get("age")
    gender = request.form.get("gender")
    phone = request.form.get("phone")
    new_person = {
        "person_id": person_id,
        "name": name,
        "age": age,
        "gender": gender,
        "phone": phone
    }
    try:
        result = people.insert_one(new_person)
    except pymongo.errors.DuplicateKeyError:
        return jsonify({"error": "Person with the same ID already exists."}), 400
    return jsonify({"person_id": person_id, "message": "Person created succefully!"})

# Update person data
@app.route("/person/<person_id>/update", methods=["POST"])
def update_person(person_id):
    db = get_db()
    people = db["myPeople"]
    person_id = request.form.get("person_id")
    name = request.form.get("name")
    age = request.form.get("age")
    gender = request.form.get("gender")
    phone = request.form.get("phone")
    person_data = {
        "name": name,
        "age": age,
        "gender": gender,
        "phone": phone
    }
    #result = people.update_one({"_id": ObjectId(person_id)}, {"$set": person_data})
    result = people.update_one({"person_id": person_id}, {"$set": person_data})
    if result.modified_count > 0:
        return jsonify({"message": "Person updated successfully!"}), 200
    else:
        return jsonify({"error": "Failed to update person."}), 500

# Delete some person.
@app.route("/person/<person_id>/delete", methods=["DELETE"])
def delete_person(person_id):
    #person_id = request.form.get("person_id")
    db = get_db()
    people = db["myPeople"]
    #try:
    #    person_id = ObjectId(person_id)
    #except bson.errors.InvalidId:
    #    return jsonify({"error": "invaild object id."}), 400
    person = people.find_one({"person_id": person_id})
    if person is None:
        return jsonify({"error": "Person not found."}), 404
    result = people.delete_one({"person_id": person_id})
    if result.deleted_count == 0:
        return jsonify({"error": "Failed to delete person."}), 500
    return jsonify({"message": "Person deleted successfully!"}), 200

@app.after_request
def add_header(response):
    response.cache_control.no_cache = True
    response.headers['Cache-control'] = 'no-store'
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
