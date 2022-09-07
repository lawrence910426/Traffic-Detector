from flask import Flask, request, jsonify

@app.route('/progress', methods=['GET'])
def getProgress():
    return jsonify({ "msg": "OK" })
