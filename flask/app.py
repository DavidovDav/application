from flask import Flask, render_template, request, url_for, redirect, jsonify
from pymongo import MongoClient

# Create a new Flask application and assigns it to the variable 'app'.
app = Flask(__name__)
# Create and execute mongodb
client = MongoClient(host="mongo", 
                    port=27017, 
                    username="root", 
                    password="pass", 
                    authSource="admin")
# Connect to data base then to collection (/myMongo/people)
#people = client["myMongo"]["people"]
db = client["myMongo"]
people = db["myPeople"]

@app.route("/health")
def health_check():
    print("The web site is working!")
    return jsonify({'message': 'Healthy'})

# Home page.
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/hello")
def hello():
    return "Hello! v0.1.0"

@app.route("/person/<int:person_id>", methods=["GET"])
def get_person(person_id):
    result = people.find_one({"person_id": Objectid(person_id)})
    if result is None:
        return jsonify({"error": "Person not found"}), 404
    return jsonify(result), 200

# To get the all peoples in data base.
@app.route("/person/get_all", methods=["GET"])
def get_peoples():
    results = people.find({})
    return jsonify(list(results)), 200

# Create some person.
@app.route("/person", methods=["POST"])
def create_person():
    data = request.json()
    person_id = data['person_id']
    name = data['name']
    age = data['age']
    gender = data['gender']
    phone = data['phone']
    new_person = {"person_id": person_id, "name": name, "age": age, "gender": gender, "phone": phone}
    people.insert_one(new_person)
    return "Person created successfully!", 201

# Update person data
@app.route("/person/<int:person_id>", methods=["PUT"])
def update_person(person_id):
    person_data = request.json
    result = people.update_one({"person_id": Objectid(person_id)}, {"$set": person_data})
    if result.matched_count == 0:
        return jsonify({"error": "Person not found"}), 404
    return jsonify({"message": "Person updated succesfully"}), 200

# Delete some person.
@app.route("/person/<int:person_id>", methods=["DELETE"])
def delete_person(person_id): 
    result = people.delete_one({"person_id": Objectid(person_id)})
    if result.delete_count == 0:
        return jsonify({"error": "Person not fount"}), 404
    return jsonify({"message": "Person deleted successfully"}), 200
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)