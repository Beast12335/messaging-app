from flask import Flask, render_template, request, redirect, url_for
import os
import random
import psycopg2
from psycopg2 import sql
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Function to get random names
def get_random_name():
    names = [
        "Cool Panda", "Happy Turtle", "Red Fox", "Smart Rabbit", "Curious Cat",
        "Brave Lion", "Witty Owl", "Mighty Elephant", "Quiet Bear", "Graceful Swan",
        "Bold Eagle", "Noble Deer", "Friendly Dolphin", "Clever Monkey", "Playful Seal",
        "Swift Cheetah", "Charming Peacock", "Wise Owl", "Gentle Giraffe", "Silent Wolf",
        "Cheerful Koala", "Energetic Squirrel", "Loyal Dog", "Fierce Tiger", "Calm Whale",
        "Elegant Flamingo", "Speedy Falcon"
    ]
    return random.choice(names)

# Function to connect to the PostgreSQL database
def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

# Initialize database with a messages table
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            name TEXT,
            message TEXT,
            image TEXT
        );
    ''')
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form['message']
        name = get_random_name()

        if 'image' not in request.files:
            image_filename = None
        else:
            image = request.files['image']
            if image and allowed_file(image.filename):
                image_filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            else:
                image_filename = None

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (name, message, image) VALUES (%s, %s, %s)", (name, message, image_filename))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name, message, image FROM messages ORDER BY id DESC')
    messages = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
