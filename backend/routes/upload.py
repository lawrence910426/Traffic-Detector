from flask import Flask, flash, request, redirect, url_for, json, jsonify
import hashlib
from app import app
from werkzeug.utils import secure_filename
import os
import time
import subprocess
import uuid

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    extension = file.filename.split('.')[-1]

    unique_id = str(uuid.uuid4())
    fname = unique_id + "." + extension
    path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
    file.save(path)

    return jsonify({ "id": fname })
