iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 3001
iptables -t nat -L --line-numbers
# sudo iptables -D PREROUTING 2 -t nat
