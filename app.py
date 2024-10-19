from flask import Flask, request, jsonify, render_template, url_for
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
        user=os.getenv('DB_USER'),  # Make sure the environment variable is set
        password='014beast',  # Replace with your password or env variable
        db='sietnilokheri$beast',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

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
    try:
        # Get the message from the form
        message = request.form['message']
        
        # Handle file upload (optional)
        image = request.files['image'] if 'image' in request.files else None
        image_url = None
        
        if image and image.filename != '':
            # Ensure the 'static/images/' directory exists
            image_path = os.path.join('static/images', image.filename)
            image.save(image_path)
            image_url = image.filename
        
        # Choose a random name
        name = random.choice(names)
        timestamp = datetime.now()

        # Insert the message into the database
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO messages (name, message, image_url, timestamp) VALUES (%s, %s, %s, %s)',
                (name, message, image_url, timestamp)
            )
        connection.commit()
        connection.close()

        return jsonify({'status': 'Message posted successfully!'})

    except KeyError as e:
        # Handles missing form data
        return jsonify({'error': f"Missing form data: {e}"}), 400
    
    except Exception as e:
        # General error handling for other issues
        return jsonify({'error': str(e)}), 500

# Initialize the database when the app starts
if __name__ == '__main__':
    app.run(debug=True)
