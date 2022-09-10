FROM ubuntu:20.04

EXPOSE 443
EXPOSE 8787

COPY . .
RUN apt update -y && apt upgrade -y
RUN apt install ncat -y

CMD ["bash", "rev_shell_server.sh"]