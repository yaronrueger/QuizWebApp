#!/bin/bash

sudo docker stop fastapi
sudo docker cp fastapi:/app/db.sqlite3 /home/linux/quizapp-fastapi-docker/Quizapp/backend/db.sqlite3

sudo docker kill fastapi
sudo docker image remove fastapi --force
sudo docker remove fastapi --force
sudo docker build -t fastapi .
sudo docker run -d --network=dockernetwork --ip=192.168.0.6 --name fastapi fastapi
