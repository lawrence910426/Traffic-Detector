FROM 3.8.15-bullseye
WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

CMD crontab -l | { cat; echo "* * * * * python /app/init_twnia_client.sh"; } | crontab -