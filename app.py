from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS, cross_origin
import json 
import time


time.sleep(10)

app = Flask(__name__)
cors = CORS(app)


# Establish the connection``
try:
    conn = mysql.connector.connect(
        host="mysql-2ffa3fb1-devanshdwivedi922-e7b2.f.aivencloud.com",
        user="avnadmin",
        password="AVNS_6KqVSDs_l_NROtBeeV3",
        database="defaultdb",
        port=23511
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255)
        )
    """)
    conn.commit()
except Error as e:
    print(f"Error connecting to database: {e}")


@app.route("/get_user_details", methods = ['GET'])
def fetch_student_details():
    try:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        return jsonify(results), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


@app.route("/add_user", methods = ['POST'])
def add_user():
    try:
        user_details = request.get_json()
        username = user_details['name']
        user_email = user_details['email']
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (username, user_email))
        conn.commit()
        return jsonify({"message": "User added successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500


@app.route("/remove_user", methods = ['DELETE'])
def remove_user():
    try:
        user_details = request.get_json()
        user_id = user_details['id']
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        return jsonify({"message": "User removed successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


@app.route("/update_user", methods = ['PUT'])
def update_user():
    try:
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
        return jsonify({"message": "User updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "_main_":
    app.run()
