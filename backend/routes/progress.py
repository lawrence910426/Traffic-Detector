from flask import Flask, request, jsonify
from app import app
import subprocess

@app.route('/progress', methods=['GET'])
def getProgress():
    task_id = request.args.get('taskId')

    with open('scripts/get_progress.sh', 'r') as file:
        bash_template = file.read()
        bash_command = bash_template.format(
            id=task_id
        )

    out = subprocess.check_output(
        bash_command, 
        shell=True
    )
    out = out.decode('utf-8')
    print("[Out]", out)

    progress = out.split("---")[-1]
    return jsonify({ "progress": progress })
