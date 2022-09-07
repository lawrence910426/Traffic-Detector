from flask import Flask, request, jsonify


@app.route('/first_frame', methods=['GET'])
def getFirstFrame():
    video_id = request.form['id']

    return jsonify({ "msg": "OK" })