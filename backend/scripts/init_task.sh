echo "nohup conda run -n detector python deepsort-counter.py videos/{video_id} --detector_line {detector} --output_name {output_id} --stable_period {stabilization} &> /dev/null & ln -s ../output/{output_id}.out scripts/slurm-{uuid}.out & exit" | nc {LOCAL_IP} 8787