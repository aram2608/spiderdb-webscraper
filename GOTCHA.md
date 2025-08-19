# Quality of Life Gotchas for future reference

Pointing mongodb to custom directories (uses /data/db by default.)
```
# 1) Make a data dir you own
mkdir -p ~/mongodb/data
chmod 700 ~/mongodb/data

# 2) Start mongod and point it at that dir
mongod --dbpath ~/mongodb/data

# Leave that terminal running. In a new tab:
mongosh

# Mongosh interacive terminal
test> use spiderdb
switched to db spiderdb
books_db> db.createCollection("books")
{ ok: 1 }
books_db> show collections
books
books_db>
```