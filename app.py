from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os


app = Flask(__name__, template_folder='')
load_dotenv()
# MongoDB Configuration
# Connecting to MongoDB
username = os.getenv('MONGODB_USERNAME')
password = os.getenv('MONGODB_PASSWORD')
cluster_address = os.getenv('MONGODB_CLUSTER_ADDRESS')
database = os.getenv('MONGODB_DATABASE')
connection_string = f'mongodb+srv://{username}:{password}@{database}.{cluster_address}/?retryWrites=true&w=majority'
client = MongoClient(connection_string)

# Creating a database and collection instance
db = client['Internship']
collection = db['Blog']


@app.route('/')
def index():
    # Retrieve all blog posts from the database
    posts = collection.find()
    return render_template('index.html', posts=posts)


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        # Get the form data
        title   = request.form['title']
        content = request.form['content']
        date = datetime.now()

        # Create a new post document
        post = {'title': title, 'content': content, 'date': date}

        # Insert the post into the database
        collection.insert_one(post)

        return redirect('/')

    return render_template('add_post.html')

@app.route('/')
def posts():
    posts = [...]  # Retrieve your blog posts from the database
    return render_template('index.html', posts=posts)

@app.route('/post/<post_id>')
def show_post(post_id):
    post = [...]  # Retrieve the specific post from the database based on post_id
    return render_template('post.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)
