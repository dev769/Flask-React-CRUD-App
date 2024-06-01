from flask import Flask, jsonify, request
import mysql.connector

from flask_cors import CORS, cross_origin
import json 
import time

from dotenv import load_dotenv
load_dotenv()

import os
HOST = os.getenv("HOST")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")
PORT = os.getenv("PORT")


time.sleep(10)

app = Flask(__name__)
cors = CORS(app)

# Establish the connection
conn = mysql.connector.connect(
    host=HOST,         # Replace with your host
    user=USER,      # Replace with your username
    password=PASSWORD,  # Replace with your password - dwivedi@123
    database=DATABASE,  # Replace with your database name
    port = PORT
)

# Create a cursor object
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255)
    )
""")

conn.commit()


@app.route("/get_user_details", methods = ['GET'])
def fetch_student_details():
    cursor.execute(f"SELECT * FROM users")
    results = cursor.fetchall()
    return json.dumps(results, indent=4, sort_keys=True, default=str)


@app.route("/add_user", methods = ['POST'])
def add_user():
    user_details = request.get_json() 
    username = user_details['name']
    user_email = user_details['email']
    print(username, user_email)
    cursor.execute(f"INSERT INTO users (name, email) VALUES ('{username}','{user_email}')")
    conn.commit()
    return "Success"


@app.route("/remove_user", methods = ['DELETE'])
def remove_user():
    user_details = request.get_json() 
    user_id = user_details['id']
    cursor.execute(f"DELETE FROM users WHERE id = {user_id}")
    conn.commit()
    return "User Removed"


@app.route("/update_user", methods = ['PUT'])
def update_user():
    user_details = request.get_json() 
    print(user_details)
    user_id = user_details['id']
    if 'name' in user_details and 'email' in user_details:
        username= user_details['name']
        useremail= user_details['email']
        query_update = f"name = '{username}', email = '{useremail}'"
    elif 'name' in user_details:
        username = user_details['name']
        query_update = f"name = '{username}'"
    elif 'email' in user_details:
        useremail = user_details['email']
        query_update = f"email = '{useremail}'"
        
    print(query_update)
    cursor.execute(f"UPDATE users SET {query_update} WHERE id = {user_id}")
    conn.commit()
    return "User Updated"



if __name__ == "_main_":
    app.run()
