while true; do ncat -l -e '/usr/bin/ncat -l localhost 8787' localhost 8080; done
