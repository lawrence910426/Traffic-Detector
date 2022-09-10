from flask import Flask, flash, request, redirect, url_for, json, jsonify
import hashlib
from app import app

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        
        m = hashlib.sha256()
        m.update(filename)
        fname = m.hexdigest()

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
        return jsonify({ "id": fname })
    else:
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
        </form>
        '''