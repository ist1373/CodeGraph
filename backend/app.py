import os
from typing import cast

from fastapi import FastAPI, HTTPException,Query
from neo4j import GraphDatabase
from contextlib import asynccontextmanager
from neo4j_service import Neo4jService
from embedding_service import EmbeddingService
from logging_utils import configure_logger
from fastapi.middleware.cors import CORSMiddleware

embedder_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    app.state.neo4j_service = Neo4jService()
    app.state.embedding_service = EmbeddingService()
    app.state.embedding_logger = configure_logger("embedding_logs","./logs")
    app.state.neo4j_logger = configure_logger("neo4j_logs","./logs")
    yield
    app.state.neo4j_service.driver.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with the React app's URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
def root():
    return {"message": "Backend is running!"}

@app.get("/relations-count")
def get_relations_count():
    try:
        toral_rels = app.state.neo4j_service.get_total_relationships(logger = app.state.neo4j_logger)
        return {"Total number of relationships":toral_rels}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data from Neo4j: {e}")

@app.get("/nodes-count")
def get_nodes_count():
    try:
        toral_nodes = app.state.neo4j_service.get_total_nodes(logger = app.state.neo4j_logger)
        return {"Total number of nodes":toral_nodes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data from Neo4j: {e}")


@app.get("/import-nodes")
def import_nodes(
    start: int = Query(default=0, description="Description of param1"),
    end: int = Query(default=1000, description="Description of param2"),
):
    try:
        toral_new_nodes = app.state.neo4j_service.import_nodes(int(start),int(end),logger = app.state.neo4j_logger)
        return {"Total number of newly added nodes":toral_new_nodes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data from Neo4j: {e}")
    
@app.get("/import-relations")
def import_relations(
    start: int = Query(default=0, description="Description of param1"),
    end: int = Query(default=1000, description="Description of param2"),
):
    try:
        status = app.state.neo4j_service.import_relations(int(start),int(end),logger = app.state.neo4j_logger)
        return {"Relations have been added:":status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data from Neo4j: {e}")

@app.get("/create-index")
def create_index_on_uuid():
    try:
        status = app.state.neo4j_service.create_index(logger = app.state.neo4j_logger)
        return {"Indexing status":status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data from Neo4j: {e}")

@app.get("/create-semantic-index")
def create_semantic_index():
    try:
        status = app.state.neo4j_service.create_sematic_index(logger = app.state.neo4j_logger)
        return {"Semantic search has been created successfully":status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data from Neo4j: {e}")

@app.get("/semantic-path-search")
def semantic_path_search(query: str = Query(..., description="Query string for semantic search")):
    try:
        embeddings = app.state.embedding_service.get_embeddings([query],app.state.embedding_logger)[0]
        
        paths = app.state.neo4j_service.retrive_semantic_paths(embeddings = embeddings,logger = app.state.neo4j_logger)
        print(paths)
        return {"results":paths}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data from Neo4j: {e}")

@app.get("/delete-all")
def delete_all():
    try:
        status = app.state.neo4j_service.delete_all(logger = app.state.neo4j_logger)
        if status:
            return {"All nodes have been deleted":status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data from Neo4j: {e}")



