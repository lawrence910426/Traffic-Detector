from flask import Flask, request, jsonify

@app.route('/task_id', methods=['GET'])
def getTaskId():
    return jsonify({ "msg": "OK" })