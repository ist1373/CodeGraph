# Use the official Neo4j image
FROM neo4j:5.20.0

# Install APOC plugin
# ENV NEO4J_APOC_JAR=/plugins/apoc-5.20.0.jar
COPY plugins/apoc-5.20.0.jar /plugins/

# Install GDS plugin
# ENV NEO4J_GDS_JAR=/plugins/gds-2.8.0.jar
COPY plugins/gds-2.8.0.jar /plugins/

# Make sure to enable the plugins in the Neo4j configuration
COPY neo4j.conf /var/lib/neo4j/conf/neo4j.conf
COPY apoc.conf /var/lib/neo4j/conf/apoc.conf

# Expose the Neo4j port
EXPOSE 7474 7687