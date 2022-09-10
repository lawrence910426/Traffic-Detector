from flask import Flask, request, jsonify
import subprocess

@app.route('/task_id', methods=['GET'])
def getTaskId():
    form = request.form
    video_id = form['id']
    stabilization = form['stabilization']
    detector = f'{form['detector']['x1']},{form['detector']['y1']},{form['detector']['x2']},{form['detector']['y2']}'
    bashCommand = f'export STABLE_PERIOD={stabilization} && export DETECTOR_LINE={detector} && export OUTPUT_NAME={video_id} && export VIDEO_ID={video_id} && sbatch run.sh'

    process = subprocess.run(bashCommand.split(), stdout=subprocess.PIPE, capture_output=True)
    out, err = process.stdout, process.stderr
    slurm_id = out.split(" ")[-1]
    return jsonify({ "id": slurm_id })
