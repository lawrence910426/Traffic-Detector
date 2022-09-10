import os
from flask import Flask, flash, request, redirect, url_for, json, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/tmp/"

from routes import first_frame, flow, progress, task_id, upload
