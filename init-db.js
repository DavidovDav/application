db = db.getSiblingDB("mongo");
db.mongo.drop()

db.mongo.insertMany([
    {
       "id": 1,
       "name": "Lion",
       "type": "Wild" 
    },
    {
        "id": 2,
        "name": "Cow",
        "type": "Domestic" 
    }
]);