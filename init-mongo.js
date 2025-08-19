// init-mongo.js
db = db.getSiblingDB("spiderdb");
db.createCollection("books");
db.books.insertOne({ __seed: true, createdAt: new Date() });