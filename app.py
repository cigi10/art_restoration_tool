from flask import Flask, request, render_template, redirect, url_for
import os
import cv2

app = Flask(__name__)

# Path to save uploaded and restored images
UPLOAD_FOLDER = 'uploads/'
RESTORED_FOLDER = 'restored/'

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESTORED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file without a name
    if file.filename == '':
        return 'No selected file', 400
    
    # Validate file type
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        return 'Unsupported file type. Please upload an image.', 400

    # Save uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Restore the image
    restored_image_path = os.path.join(RESTORED_FOLDER, file.filename)
    restore_image(file_path, restored_image_path)

    # Redirect to result page instead of sending file directly
    return redirect(url_for('show_result', filename=file.filename))

@app.route('/result/<filename>')
def show_result(filename):
    # Correctly construct the URL to access the restored image
    restored_image_url = url_for('static', filename=f'restored/{filename}')
    return render_template('result.html', restored_image=restored_image_url)

def restore_image(input_path, output_path):
    # Restore image logic
    image = cv2.imread(input_path)

    if image is None:
        raise ValueError("Could not read the image file.")
    
    # Example restoration logic (Gaussian Blur in this case)
    restored_image = cv2.GaussianBlur(image, (5, 5), 0)
    cv2.imwrite(output_path, restored_image)

if __name__ == '__main__':
    app.run(debug=True)
