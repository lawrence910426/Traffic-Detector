# This is an example script to execute remote shell command

echo "cd ../image-detector/scripts/; sbatch sbatch_script.sh; exit" | nc localhost 8787
