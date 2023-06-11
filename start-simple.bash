#! /bin/bash
# assuming that docker daemon is running
# script to setup 3 nodes and populate initial database
echo "Creating all the nodes..."
#first node
docker run --name alpha -p 9042:9042 -d cassandra:latest > /dev/null
sleep 1
INSTANCE_ALPHA=$(docker inspect --format="{{ .NetworkSettings.IPAddress }}" alpha)
sleep 1
printf "Node Alpha:\t ${INSTANCE_ALPHA}\n"

sleep 60

python3 initial_setup.py
