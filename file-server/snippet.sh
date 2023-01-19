docker run -it -p 139:139 -p 445:445 -d dperson/samba -u "flask;2rjurrru" -u "compute;2rjurrru" -s "public;/share;yes;no;no;all;all;all;"
# ssh into docker. Then chmod /share to 777.
sudo mount -t cifs -o user=flask,password=2rjurrru //127.0.0.1/public /mnt/local_share/
sudo umount /mnt/local_share