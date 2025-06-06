# init_db.py
import sqlite3

connection = sqlite3.connect("student.db")
cursor = connection.cursor()

# Create the table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    enrollment TEXT,
    standard TEXT,
    subject TEXT,
    city TEXT,
    hobby TEXT
)
""")

# Insert some sample data
cursor.executemany("""
INSERT INTO students (name, enrollment, standard, subject, city, hobby)
VALUES (?, ?, ?, ?, ?, ?)
""", [
    ("Vandan", "EN1234", "12th", "Physics", "Navsari", "Drawing"),
    ("Krishna", "EN5678", "11th", "Chemistry", "Surat", "Reading"),
    ("Neha", "EN9101", "10th", "Maths", "Valsad", "Cycling"),
    ("Neva", "EN9102", "10th", "Maths", "Valsad", "Cycling"),
    ("Nev", "EN9202", "10th", "science", "Valsad", "Cycling")
])


connection.commit()
connection.close()

# query="SELECT * FROM students WHERE name LIKE '%Vandan%';"
# connection = sqlite3.connect("student.db")
# cursor = connection.cursor()
# cursor.execute(query)
# rows = cursor.fetchall()
# for row in rows:
#     print(row)

# print("Database initialized successfully.")
