from flask import Flask, render_template, request, url_for, redirect, jsonify
#from flask_pymongo import PyMongo
from pymongo import MongoClient

# Connect to data base and else.
app = Flask(__name__)   # Create a new Flask application and assigns it to the variable 'app'.

# Create and execute mongodb
def get_db():
    client = MongoClient(host='mongo',
                        port=27017,
                        user='root',
                        password='pass',
                        authoSource='admin')
    db = client["mongo"]
    return db
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mongo"         # Sets a configuration option for the Flask application that specifies the URI of the MongoDB server to connect to.
#pp.config['JSONIFY_PRETTYPRINT_REGULAR'] = True                     # Sets a configuration option for the Flask application that enables "pretty printing" of JSON responses.
#mongo = PyMongo(app)                                                # Creates a new instance of PyMongo and associates it with the Flask application.
#client = MongoClient(app.config["MONGO_URI"])                       # Creates a new instance of MongoClient which is a class of pymongo package.
#db = client.mongo                                                   # Connect to the "db" database.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# The home page
@app.route("/hello")
def home():
    return "Hello David! v0.1.0"

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