import os
import re
import cv2

# Flask utils
from flask import Flask, flash, request, render_template, send_from_directory
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# Define a flask app
app = Flask(__name__, static_url_path='')
app.secret_key = os.urandom(24)

app.config['ENHANCED_FOLDER'] = 'images'
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/uploads/<filename>')
def upload_img(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/images/<filename>')
def enhanced_img(filename):
    return send_from_directory(app.config['ENHANCED_FOLDER'], filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def cartoonize_2(img):
    # Convert the input image to gray scale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # stylization of image
    img_style = cv2.stylization(img, sigma_s=150, sigma_r=0.25)

    return img_style


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/history', methods=['GET'])
def history():
    images = os.listdir(app.config['UPLOAD_FOLDER'])

    # Remove non-image files
    images = [image for image in images if allowed_file(image)]

    # Extract the desired image name format using regex
    pattern = r'(Cyst|Normal)(?:-_)?(?:_)?(\d+)(?:_)?(?:Grainy)?'
    images_with_names = []
    for image in images:
        matches = re.findall(pattern, image)
        if matches:
            name = f'{matches[0][0]} {matches[0][1]}'
            images_with_names.append((image, name))

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
    enhanced_files = []

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

            enhanced = cartoonize_2(img)
            en_filename = filename + "_enhanced.jpg"
            enhanced_path = os.path.join(app.config['ENHANCED_FOLDER'], en_filename)
            cv2.imwrite(enhanced_path, enhanced)

            uploaded_files.append(filename)
            enhanced_files.append(en_filename)

    return render_template('predict.html', uploaded_files=uploaded_files, enhanced_files=enhanced_files)


if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=8080)
