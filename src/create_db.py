import sqlite3

# Connect/create database
conn = sqlite3.connect("database/n100.db")

# Read schema file
with open("database/schema.sql", "r", encoding="utf-8") as f:
    schema = f.read()

# Execute schema
conn.executescript(schema)

print("Database and tables created successfully!")

conn.close()