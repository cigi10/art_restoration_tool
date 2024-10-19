from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def denoise_image(image):
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    image = cv2.imread(file_path)
    denoised_image = denoise_image(image)

    denoised_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'denoised_' + filename)
    cv2.imwrite(denoised_file_path, denoised_image)

    return jsonify({'denoised_image_url': denoised_file_path})

if __name__ == '__main__':
    app.run(debug=True)
