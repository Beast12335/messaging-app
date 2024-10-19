from flask import Flask, render_template, request, redirect, url_for
import os
import random
import pymysql
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Database connection function
def get_db_connection():
    connection = pymysql.connect(
        host='sietnilokheri.mysql.pythonanywhere-services.com',
        user=os.getenv('DB_USER'),  # Ensure DB_USER is set in your .env file
        password='014beast',  # Ensure DB_PASS is set in your .env file
        db='sietnilokheri$beast',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

# Check if the uploaded file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Function to generate a random name for each post
def get_random_name():
    names = [
        "Cool Panda", "Happy Turtle", "Red Fox", "Smart Rabbit", "Curious Cat", 
        "Mysterious Falcon", "Silent Owl", "Shadow Panther", "Lone Wolf"
    ]
    return random.choice(names)

# Route for homepage and message submission
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form['message']
        name = get_random_name()
        timestamp = datetime.now()

        # Check for image upload
        if 'image' not in request.files:
            image_filename = None
        else:
            image = request.files['image']
            if image and allowed_file(image.filename):
                image_filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            else:
                image_filename = None

        # Insert the message into the MySQL database
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute('''
                INSERT INTO messages (name, message, image_url, timestamp) 
                VALUES (%s, %s, %s, %s)
            ''', (name, message, image_filename, timestamp))
        connection.commit()
        connection.close()

        # Redirect back to the homepage after message submission
        return redirect(url_for('index'))

    # Retrieve all messages from the MySQL database
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT name, message, image_url, timestamp FROM messages ORDER BY timestamp DESC')
        messages = cursor.fetchall()
    connection.close()

    # Render the template with the messages
    return render_template('index.html', messages=messages)


if __name__ == '__main__':
    # Ensure the database is initialized (you can comment this out if not needed anymore)
    #init_db()
    app.run(debug=True)
