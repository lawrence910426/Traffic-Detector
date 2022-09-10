from flask import Flask, request, jsonify

@app.route('/flow', methods=['GET'])
def getFlow():
    task_id = request.form['taskId']

    with open('scripts/get_result.sh', 'r') as file:
        bash_template = file.read()
        bash_command = bash_template.format(
            id=task_id
        )

    process = subprocess.run(bashCommand.split(), stdout=subprocess.PIPE, capture_output=True)
    out, err = process.stdout, process.stderr
    
    print(out)
    progress = out.split("---")[-1]
    return flow