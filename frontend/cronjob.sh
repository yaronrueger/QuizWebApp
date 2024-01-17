#!/bin/bash

REPO_PATH="/home/linux/svelte-quizapp-docker"
DOCKERFILE_PATH="/home/linux/svelte-quizapp-docker/frontend"
CONTAINER_NAME="svelte"
IMAGE_NAME="svelte"        

CURRENT_HASH=$(git -C "$REPO_PATH" rev-parse HEAD)

git -C "$REPO_PATH" pull
NEW_HASH=$(git -C "$REPO_PATH" rev-parse HEAD)

if [ "$CURRENT_HASH" != "$NEW_HASH" ]; then
    sudo docker stop "$CONTAINER_NAME" 2>/dev/null
    sudo docker rm "$CONTAINER_NAME" 2>/dev/null
    sudo docker build -t "$IMAGE_NAME" "$DOCKERFILE_PATH"
    sudo docker run -d --network=dockernetwork --ip=192.168.0.8 --name "$CONTAINER_NAME" "$IMAGE_NAME"
    wall Container geupdated #lol
fi
#wall Container nicht geupdated
