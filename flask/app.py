from flask import Flask, render_template, request, url_for, redirect, jsonify, Response
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

# Home page.
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/hello")
def hello():
    return "Hello! v0.1.0"

@app.route("/person/<int:person_id>", methods=["GET"])
def get_person(person_id):
    person = people.find_one({"person_id": person_id})
    if person:
        return jsonify(person), 200
    else:
        return "Person not found.", 404


# To get the all peoples in data base.
@app.route("/person", methods=["GET"])
def get_peoples():
    results = people.find({})
    return jsonify(list(results)), 200

# Create some person.
@app.route("/person/<int:person_id>", methods=["POST"])
def create_person(person_id):
    data = request.get_json()
    person_id = data['person_id']
    name = data['name']
    age = data['age']
    gender = data['gender']
    phone = data['phone']
    new_person = {
        "person_id": person_id,
        "name": name,
        "age": age,
        "gender": gender,
        "phone": phone
        }
    result = people.insert_one(new_person)
    location = url_for('get_person', person_id=person_id, _exteranl=True)
    return Response(status=201,headers={"Location": location})

# Update person data
@app.route("/person/<int:person_id>", methods=["PUT"])
def update_person(person_id):
    person_data = request.get_json()
    result = people.update_one({"person_id": person_id},{"$set": person_data})
    if result.matched_count == 0:
        return jsonify({"error": "Person not found"}), 404
    return jsonify({"message": "Person updated succesfully"}), 200

# Delete some person.
@app.route("/person/<int:person_id>", methods=["DELETE"])
def delete_person(person_id): 
    result = people.delete_one({"person_id": person_id})
    if result.delete_count == 0:
        return jsonify({"error": "Person not fount"}), 404
    return jsonify({"message": "Person deleted successfully"}), 200

@app.after_request
def add_header(response):
    response.cache_control.no_cache = True
    response.headers['Cache-control'] = 'no-store'
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)