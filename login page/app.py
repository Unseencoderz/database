from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

app = Flask(__name__)
app.static_folder = 'static'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Set up MongoDB Atlas connection (replace with your connection string)
uri = "mongodb+srv://unseencoderz:mongo%402213591@cluster0.pfkqmli.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.get_database("filedata")

# Create the 'uploads' directory if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    collection = db['mycollection']
    entries = collection.find()
    return render_template('index.html', entries=entries)

@app.route('/submit', methods=['POST'])
def submit():
    file = request.files['file']
    if file:
        filename = file.filename
        # Save the uploaded file to the 'uploads' folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        collection = db['mycollection']
        data = {'name': filename}
        collection.insert_one(data)

    return redirect(url_for('index'))

@app.route('/uploads/<filename>', methods=['GET'])
def download_file(filename):
    # Send the uploaded file for download
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
