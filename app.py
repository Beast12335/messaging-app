from flask import Flask, request, jsonify, render_template
import pymysql
import os
from dotenv import load_dotenv
from datetime import datetime
import random

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Function to establish a MySQL database connection
def get_db_connection():
    connection = pymysql.connect(
        host='sietnilokheri.mysql.pythonanywhere-services.com',
        user=os.getenv('DB_USER'),  # Ensure you use environment variables here
        password=os.getenv('DB_PASSWORD'),
        db='sietnilokheri$beast',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

# Function to initialize the database (create the table if it doesn't exist)
def init_db():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                message TEXT,
                image_url VARCHAR(255),
                timestamp DATETIME
            )
        ''')
    connection.commit()
    connection.close()

# List of random names to assign to posts
names = [
    "Mysterious Falcon", "Silent Owl", "Shadow Panther", "Lone Wolf",
    "Crimson Phoenix", "Golden Eagle", "Iron Tiger", "Blue Dragon",
    "Night Hawk", "Stealth Fox", "Emerald Serpent", "Fire Lion", 
    "Black Stallion", "White Wolf", "Scarlet Raven", "Ghost Cat",
    "Fierce Leopard", "Thunder Bear", "Wind Dancer", "Storm Crow",
    "Dusk Rider", "Silver Shark", "Steel Cobra", "Bronze Raven", 
    "Swift Eagle"
]

# Route to display messages and form for new message submission
@app.route('/')
def index():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM messages ORDER BY timestamp DESC')
        messages = cursor.fetchall()
    connection.close()
    return render_template('index.html', messages=messages)

# Route to handle message submission
@app.route('/submit', methods=['POST'])
def submit_message():
    message = request.form['message']
    image_url = request.form['image_url']
    name = random.choice(names)
    timestamp = datetime.now()

    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO messages (name, message, image_url, timestamp) VALUES (%s, %s, %s, %s)',
                       (name, message, image_url, timestamp))
    connection.commit()
    connection.close()

    return jsonify({'status': 'Message posted successfully!'})

# Initialize the database when the app starts
if __name__ == '__main__':
    init_db()  # Ensure the database is initialized
    app.run(debug=True)
