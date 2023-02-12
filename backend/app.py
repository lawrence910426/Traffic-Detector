import os
from flask import Flask, flash, request, redirect, url_for, json, jsonify
from werkzeug.utils import secure_filename

app = Flask(
    __name__,
    static_folder='/tmp/',
    static_url_path='/static'
)
app.config['UPLOAD_FOLDER'] = "/mnt/video-in/"
app.config['STATIC_URL'] = os.environ['BACKEND_HOST'] + "static/"

from routes import first_frame, query_task, init_task, upload
