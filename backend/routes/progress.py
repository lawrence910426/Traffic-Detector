from flask import Flask, request, jsonify
from app import app

@app.route('/progress', methods=['GET'])
def getProgress():
    task_id = request.form['taskId']

    with open('scripts/get_progress.sh', 'r') as file:
        bash_template = file.read()
        bash_command = bash_template.format(
            id=task_id
        )

    process = subprocess.run(bashCommand.split(), stdout=subprocess.PIPE, capture_output=True)
    out, err = process.stdout, process.stderr
    
    print(out)
    progress = out.split("---")[-1]
    return jsonify({ "progress": progress })
