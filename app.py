from flask import Flask, render_template, request, redirect, url_for
import os
import random
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_random_name():
    names = ["Cool Panda", "Happy Turtle", "Red Fox", "Smart Rabbit", "Curious Cat"]
    return random.choice(names)

def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, message TEXT, image TEXT)')
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
        
        conn = sqlite3.connect('database.db')
        conn.execute("INSERT INTO messages (name, message, image) VALUES (?, ?, ?)", (name, message, image_filename))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    conn = sqlite3.connect('database.db')
    cursor = conn.execute('SELECT name, message, image FROM messages ORDER BY id DESC')
    messages = cursor.fetchall()
    conn.close()

    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
