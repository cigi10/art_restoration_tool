from flask import Flask, request, render_template, redirect, url_for
import cv2
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def denoise_image(image):
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

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
        denoised_image = denoise_image(image)

        # Save denoised image
        denoised_filename = 'denoised_' + filename
        denoised_file_path = os.path.join(app.config['UPLOAD_FOLDER'], denoised_filename)
        cv2.imwrite(denoised_file_path, denoised_image)

        # Render the template with image paths
        return render_template('index.html', noisy_image=url_for('uploaded_file', filename=filename), 
                               denoised_image=url_for('uploaded_file', filename=denoised_filename))

    # Render the upload form for GET requests
    # return render_template('index.html')
    return render_template('index.html', noisy_image='true', 
                               denoised_image='true')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
