from flask import Flask, request, jsonify

@app.route('/flow', methods=['GET'])
def getFlow():
    task_id = request.form['taskId']
    process = subprocess.run([
        "cat", f"slurm-{task_id}.txt", "|", "tail", "-n", "1"
    ], stdout=subprocess.PIPE, capture_output=True)
    out, err = process.stdout, process.stderr
    
    flow = out.split("---")[0]
    return flow