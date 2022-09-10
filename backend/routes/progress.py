from flask import Flask, request, jsonify

@app.route('/progress', methods=['GET'])
def getProgress():
    task_id = request.form['taskId']
    process = subprocess.run([
        "cat", f"slurm-{task_id}.txt", "|", "tail", "-n", "1"
    ], stdout=subprocess.PIPE, capture_output=True)
    out, err = process.stdout, process.stderr
    
    progress = out.split("---")[-1]
    return jsonify({ "progress": progress })
