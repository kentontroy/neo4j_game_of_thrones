#!/bin/bash

docker run --env NEO4J_AUTH=neo4j/cloudera \
  --name game_of_thrones_neo4j \
  -p 7687:7687 \
  -p 7474:7474 \
  -d \
  neo4j
