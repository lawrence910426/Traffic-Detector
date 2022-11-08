import os
from flask import Flask, flash, request, redirect, url_for, json, jsonify
from werkzeug.utils import secure_filename

app = Flask(
    __name__,
    static_folder='/tmp/',
    static_url_path='/static'
)
app.config['UPLOAD_FOLDER'] = "/tmp/"
app.config['STATIC_URL'] = f"{os.environ['BACKEND_HOST']}static/"

from routes import first_frame, flow, progress, task_id, upload
from routes.get_youtube_video import get_auth_url, get_video_url
