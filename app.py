from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import cv2
import os
from werkzeug.utils import secure_filename
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Denoising function
def denoise_image(image):
    return cv2.fastNlMeansDenoisingColored(image, None, 5, 10, 1, 30)

# Clarity (Sharpening) function
def sharpen_image(image):
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        
        if file.filename == '':
            return redirect(request.url)

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Read and process the image
        image = cv2.imread(file_path)
        if image is None:
            return "Error: File is not a valid image"

        # Apply denoising on the image
        denoised_image = denoise_image(image)

        # Apply sharpening (clarity)
        sharpened_image = sharpen_image(denoised_image)

        # Save the final image
        final_filename = 'final_' + filename
        final_file_path = os.path.join(app.config['UPLOAD_FOLDER'], final_filename)
        cv2.imwrite(final_file_path, sharpened_image)

        # Render the template with both original and processed images
        return render_template('index.html', noisy_image=url_for('uploaded_file', filename=filename), 
                               denoised_image=url_for('uploaded_file', filename=final_filename))

    # For the GET request, display placeholders
    return render_template('index.html', noisy_image='/static/placeholder.png', 
                           denoised_image='/static/placeholder.png')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
