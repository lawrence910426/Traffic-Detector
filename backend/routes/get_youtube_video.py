from flask import Flask, flash, request, redirect, url_for, json, jsonify
import hashlib
from app import app
import os
import time
import subprocess
import pexpect
import sys

# Be ware, this is a stateful design. If the flask backend
# is scaled to multiple processes/nodes, the program would 
# fail since `handler` becomes inaccessible.
handler = None

# One must call `get_auth_url` before `get_video_url`
@app.route('/get_auth_url', methods=['GET'])
def get_auth_url():
    global handler
    
    handler = pexpect.spawn("nc " + os.environ['LOCAL_IP'] + " 8787")
    handler.logfile = sys.stdout.buffer
    
    videoId = request.args.get('videoId')
    with open('scripts/upload_youtube_video.sh', 'r') as file:
        bash_template = file.read()
        bash_command = bash_template.format(
            videoPath=videoId # "../video-detector/output/" + videoId + ".mp4"
        ).replace('\r', '').replace('\n', '')
    handler.expect("[lawrence0426@ln01-twnia2 ~]$")
    handler.sendline(bash_command)
    
    handler.expect_exact("Please visit this URL to authorize this application: ")
    url = handler.readline(1).decode('ascii').replace("\r", '').replace("\n", '')
    
    return jsonify({ "url": url })

@app.route('/get_video_url', methods=['GET'])
def get_video_url():
    global handler
    
    auth_code = request.args.get('authCode')
    handler.expect("Enter the authorization code: ")
    out = handler.sendline(auth_code)
    
    handler.expect_exact("Youtube link: ")
    url = handler.readline(1).decode('ascii').replace("\r", '').replace("\n", '')
    
    return jsonify({ "url": url })
