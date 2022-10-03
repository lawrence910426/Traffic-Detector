from flask import Flask, flash, request, redirect, url_for, json, jsonify
import hashlib
from app import app
from werkzeug.utils import secure_filename
import os
import time
import subprocess

@app.route('/upload_result_video', methods=['POST'])
def upload_result_video():
    file = request.files['file']
    fname = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))

    return jsonify({ "url": app.config['STATIC_URL'] + fname })
