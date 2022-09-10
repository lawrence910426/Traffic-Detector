from flask import Flask, request, jsonify
import subprocess

@app.route('/task_id', methods=['GET'])
def getTaskId():
    form = request.form
    video_id = form['id']
    stabilization = form['stabilization']
    detector = f'{form['detector']['x1']},{form['detector']['y1']},{form['detector']['x2']},{form['detector']['y2']}'

    with open('scripts/init_sbatch.sh', 'r') as file:
        bash_template = file.read()
        bash_command = bash_template.format(
            stabilization=stabilization,
            detector=detector,
            video_id=video_id
        )

    process = subprocess.run(bash_command.split(), stdout=subprocess.PIPE, capture_output=True)
    out, err = process.stdout, process.stderr
    
    print(out)
    slurm_id = out.split(" ")[-1]
    return jsonify({ "id": slurm_id })
