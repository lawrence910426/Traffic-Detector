from flask import Flask, request, jsonify
from app import app
import subprocess
import os

@app.route('/flow', methods=['GET'])
def getFlow():
    task_id = request.args.get('taskId')

    with open('scripts/get_result.sh', 'r') as file:
        bash_template = file.read()
        bash_command = bash_template.format(
            id=task_id,
            LOCAL_IP=os.environ['LOCAL_IP']
        )

    out = subprocess.check_output(
        bash_command, 
        shell=True
    )
    out = out.decode('utf-8')
    print("[Out]", out)
    
    out = out.split("\n")[1]
    progress = out.split("---")[-1]
    return flow
