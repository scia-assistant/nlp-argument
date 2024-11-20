const dbName = "faiss_db";

db.createUser({
  user: "admin",
  pwd: "admin123",
  roles: [{ role: "readWrite", db: dbName }]
});

db.createCollection("chunks");

print("Initialized");
