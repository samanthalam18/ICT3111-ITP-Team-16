from flask import Flask
import os

app = Flask(__name__, static_url_path='')
app.secret_key = os.urandom(24)
app.config['ENHANCED_FOLDER'] = 'images'
app.config['UPLOAD_FOLDER'] = 'uploads'