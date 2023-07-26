import os
import re
import cv2
import zipfile
import shutil
import config
from config import ALLOWED_EXTENSIONS
from app_init import app
import model
# Flask utils

from flask import flash, request, render_template, send_from_directory, send_file
from werkzeug.utils import secure_filename


@app.route('/uploads/<filename>')
def upload_img(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/images/<filename>')
def enhanced_img(filename):
    return send_from_directory(app.config['ENHANCED_FOLDER'], filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/history', methods=['GET'])
def history():
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    images_with_names = [(image, image) for image in images if allowed_file(image)]

    return render_template('history.html', images=images_with_names)


@app.route('/cyst', methods=['GET'])
def cyst():
    images = os.listdir(app.config['UPLOAD_FOLDER'])

    # Remove non-image files
    images = [image for image in images if allowed_file(image)]

    # Extract the desired image name format using regex
    pattern = r'(Cyst)(?:-_)?(?:_)?(\d+)(?:_)?(?:Grainy)?'
    images_with_names = []
    for image in images:
        matches = re.findall(pattern, image)
        if matches:
            name = f'{matches[0][0]} {matches[0][1]}'
            images_with_names.append((image, name))

    return render_template('cyst.html', images=images_with_names)


@app.route('/normal', methods=['GET'])
def normal():
    images = os.listdir(app.config['UPLOAD_FOLDER'])

    # Remove non-image files
    images = [image for image in images if allowed_file(image)]

    # Extract the desired image name format using regex
    pattern = r'(Normal)(?:-_)?(?:_)?(\d+)(?:_)?(?:Grainy)?'
    images_with_names = []
    for image in images:
        matches = re.findall(pattern, image)
        if matches:
            name = f'{matches[0][0]} {matches[0][1]}'
            images_with_names.append((image, name))

    return render_template('normal.html', images=images_with_names)


@app.route('/predict', methods=['POST'])
def predict():
    files = request.files.getlist('file')
    if not files:
        return render_template('index.html')

    uploaded_files = []
    # Process each file
    for file in files:
        if file and allowed_file(file.filename):
            # Save the file to the 'uploads' directory
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Perform image cartonization
            img = cv2.imread(file_path)
            if img is None:
                return render_template('index.html')

            # enhanced = cartoonize_2(img)
            en_filename = filename
            # enhanced_path = os.path.join(app.config['ENHANCED_FOLDER'], en_filename)
            # cv2.imwrite(enhanced_path, enhanced)

            uploaded_files.append(filename)
            
    model.runModel(app.config['UPLOAD_FOLDER'],app.config['ENHANCED_FOLDER'])
    return render_template('predict.html', uploaded_files=uploaded_files, enhanced_files=uploaded_files)


@app.route('/download_all_history', methods=['GET'])
def download_all_history():
    # Create a temporary directory to store the images
    temp_dir = 'temp_history'
    os.makedirs(temp_dir, exist_ok=True)

    # Copy all the files from the 'images' folder to the temporary directory
    image_files = os.listdir(app.config['ENHANCED_FOLDER'])
    for image_file in image_files:
        src_path = os.path.join(app.config['ENHANCED_FOLDER'], image_file)
        dst_path = os.path.join(temp_dir, image_file)
        shutil.copy2(src_path, dst_path)

    # Create a ZIP file containing all the images
    zip_filename = 'images.zip'
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, temp_dir))

    # Send the ZIP file for download
    return send_file(zip_filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=8080)
