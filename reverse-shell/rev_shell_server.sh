# This script runs on VPS of Taiwania

while true; do ncat -l -e "/usr/bin/ncat -l ${LOCAL_IP} 8787" 0.0.0.0 443; done
