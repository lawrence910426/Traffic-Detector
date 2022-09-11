from flask import Flask, request, jsonify
from app import app
import os
import cv2

@app.route('/first_frame', methods=['GET'])
def getFirstFrame():
    video_id = request.args.get('id')
    path = os.path.join(app.config['UPLOAD_FOLDER'], video_id)
    image_path = path.split(".")[0] + ".jpg"

    image_url = image_path.split('/')[-1]
    image_url = app.config['STATIC_URL'] + image_url

    vidcap = cv2.VideoCapture(path)
    success, image = vidcap.read()
    if success:
        cv2.imwrite(image_path, image)
        return jsonify({ "link": image_url })
    else:
        return jsonify({ "msg": "error, cannot capture image" })