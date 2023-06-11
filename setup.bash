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

#second node
docker run --name beta -p 9043:9042 -d -e CASSANDRA_SEEDS=$INSTANCE_ALPHA cassandra:latest > /dev/null
sleep 1
INSTANCE_BETA=$(docker inspect --format="{{ .NetworkSettings.IPAddress }}" beta)
sleep 1
printf "Node Beta:\t ${INSTANCE_BETA}\n"

sleep 60

#third node
docker run --name gamma -p 9044:9042 -d -e CASSANDRA_SEEDS=$INSTANCE_BETA cassandra:latest > /dev/null
sleep 1
INSTANCE_GAMMA=$(docker inspect --format="{{ .NetworkSettings.IPAddress }}" gamma)
sleep 1
printf "Node Gamma:\t ${INSTANCE_GAMMA}\n"

printf "(For correct performence it is advised to wait approx. 60s)\n"

python3 initial_setup.py
