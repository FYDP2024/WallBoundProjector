from flask import Flask, request, jsonify
import os
from flask_cors import CORS

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

CORS(app)

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/test', methods=['GET'])
def test_api():
    return("hello world")

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify({'message': 'File successfully uploaded'}), 200
    
    return jsonify({'message': 'Allowed file types are png, jpg, jpeg, gif'}), 400

if __name__ == '__main__':
    app.run(debug=True)