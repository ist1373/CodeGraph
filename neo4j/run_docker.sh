docker run -d \
    --network my-network -d\
    -p 7474:7474 \
    -p 7687:7687 \
    -e NEO4J_AUTH=neo4j/ilvlan549 \
    -e NEO4JLABS_PLUGINS='["apoc", "graph-data-science"]' \
    -v ./import:/import \
    -e NEO4J_dbms_directories_import=/import \
    -v $HOME/neo4j/data:/data \
    --name neo4j-container neo4j-image