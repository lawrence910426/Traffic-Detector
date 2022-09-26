# This is an example script to execute remote shell command

echo "cd ../video-detector/scripts/; sbatch sbatch_script.sh; exit" | nc ${LOCAL_IP} 8787
