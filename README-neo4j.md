## Ensure the docker container has access to the APOC core libraries 
```
docker exec -it game_of_thrones_neo4j bash 

root@8219d191653a:/var/lib/neo4j# cp ${NEO4J_HOME}/labs/apoc-5.13.0-core.jar ${NEO4J_HOME}/plugins
```
