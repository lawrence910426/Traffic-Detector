from flask import Flask, request, jsonify

@app.route('/flow', methods=['GET'])
def getFlow():
    return jsonify({ "msg": "OK" })