docker run -d -p 8000:8000 \
  -e NEO4J_URI=bolt://neo4j-container:7687 \
  -e NEO4J_USER=neo4j \
  -e NEO4J_PASSWORD=ilvlan549 \
  -e VOYAGE_API_KEY=pa-lpHvggxAmQX_QTSipVOhn7qC5Ue_9XRxT_RGwCEFRmE \
  -e EMBEDDER_MODEL=voyage-code-2 \
  --network my-network -d\
  --name backend-container backend-image