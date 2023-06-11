#! /bin/bash

echo "Cleaning the nodes..."
docker rm alpha -f 2> /dev/null
docker rm beta -f 2> /dev/null
docker rm gamma -f 2> /dev/null
docker rm /alpha -f 2> /dev/null
docker rm /beta -f 2> /dev/null
docker rm /gamma -f 2> /dev/null
echo "Finished cleaning!"
