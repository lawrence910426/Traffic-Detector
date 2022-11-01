from flask import Flask, flash, request, redirect, url_for, json, jsonify
import hashlib
from app import app
import os
import time
import subprocess
import pexpect

# Be ware, this is a stateful design. If the flask backend
# is scaled to multiple processes/nodes, the program would 
# fail since `handler` becomes inaccessible.
handler = None

# One must call `get_auth_url` before `get_video_url`
@app.route('/get_auth_url', methods=['GET'])
def upload_result_video():
    global handler

    videoId = request.args.get('videoId')
    with open('scripts/upload_video.sh', 'r') as file:
        bash_template = file.read()
        bash_command = bash_template.format(
            videoPath="../video-detector/output/" + videoId + ".mp4"
        )
    handler = pexpect.spawn(bash_command)
    handler.expect_exact("Please visit this URL to authorize this application: ")
    url = child.readline(1)
    
    return jsonify({ "url": url })

@app.route('/get_video_url', methods=['GET'])
def upload_result_video():
    global handler

    auth_code = request.args.get('authCode')
    handler.expect_exact("Enter the authorization code: ")
    out = child.sendline(auth_code)

    handler.expect_exact("Youtube link: ")
    url = child.readline(1)
    
    return jsonify({ "url": url })