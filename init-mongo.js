// init-mongo.js
db.createUser({
    user: "me",
    pwd: "pass",
    roles: [{ role: "readWrite", db: "spiderdb" }]
});

db.getSiblingDB("spiderdb").createCollection("books");