from flask import Flask, request, jsonify


@app.route('/first_frame', methods=['GET'])
def getFirstFrame():
    video_id = request.form['id']
    path = os.path.join(app.config['UPLOAD_FOLDER'], video_id)
    image_path = path.split(".")[0] + ".jpg"

    vidcap = cv2.VideoCapture(path)
    success, image = vidcap.read()
    if success:
        cv2.imwrite(image_path, image)
    
    return jsonify({ "id": image_path })