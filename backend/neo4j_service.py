from neo4j import GraphDatabase
from logging import Logger
import os
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "ilvlan549")

class Neo4jException(Exception):
    def __init__(self, message):
        super().__init__(message)
        
class Neo4jService:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def get_total_relationships(self,logger:Logger):
        # Open a session and get the total number of relationships
        def _get_total_relationships(tx):
            result = tx.run("MATCH ()-[r]->() RETURN count(r) AS total_relationships")
            return result.single()["total_relationships"]
        
        try:
            with self.driver.session() as session:
                total_relationships = session.execute_read(_get_total_relationships)
            logger.info(f"total number of relationships retrieved:{total_relationships}")
            # Print the total number of relationships
            return total_relationships
        except Exception as e:
            error_message = f"Error occurred while retrieving total number of relationships: {e}"
            logger.error(error_message)
            raise Neo4jException(error_message)


    def get_total_nodes(self,logger:Logger):
        # Open a session and get the total number of relationships
        def _get_total_nodes(tx):
            result = tx.run("MATCH (n) RETURN count(n) AS nodeCount")
            return result.single()["nodeCount"]
        try:
            with self.driver.session() as session:
                total_nodes = session.execute_read(_get_total_nodes)
            logger.info(f"total number of relationships retrieved:{total_nodes}")
            # Print the total number of relationships
            return total_nodes
        except Exception as e:
            error_message = f"Error occurred while retrieving total number of nodes: {e}"
            logger.error(error_message)
            raise Neo4jException(error_message)
        
    def import_nodes(self,start,end,logger:Logger):
        total_number_of_processed_functions = 0
        for j in range(start,end,1000):

            def create_nodes(tx):
                    query = f"""
                    WITH "file:///nodes_{j}_enhanced.json" AS url
                    CALL apoc.load.json(url) YIELD value AS data
                    UNWIND data AS item
                    CALL apoc.create.node(['code_block'], {{content:item.content,node_type:item.node_type,embedding:item.embedding,embedding_large:item.voyage_content,uuid:item.uuid,groupid:{j}}}) YIELD node
                    RETURN node
                    """
                    docs = tx.run(query)
                # return docs
            try:
                with self.driver.session() as session:
                    docs = session.execute_write(create_nodes)
                total_number_of_processed_functions += 1000
                logger.info(f"total number of processed functions:{total_number_of_processed_functions}")
            except Exception as e:
                error_message = f"Error occurred while importing nodes: {e}"
                logger.error(error_message)
                raise Neo4jException(error_message)
        return total_number_of_processed_functions

            
    def import_relations(self,start,end,logger:Logger):
        total_number_of_processed_functions = 0
        for j in range(start,end,1000):
            def _create_relationships(tx):
                
                    query = f"""
                    CALL apoc.load.json("file:///relations_{j}.json") YIELD value

                    WITH value AS relationship

                    // Match nodes based on UUIDs
                    MATCH (a:code_block {{groupid: {j},uuid: relationship.uuid_from}})
                    MATCH (b:code_block {{groupid: {j},uuid: relationship.uuid_to}})

                    // Create a relationship with a dynamic type
                    CALL apoc.create.relationship(a, relationship.relation_type, {{}}, b) YIELD rel

                    // Return the result
                    RETURN a, b, rel
                    """
                    docs = tx.run(query)
                    print(f"doc {j} has been processed.")
                # return doc
            try:
                with self.driver.session() as session:
                    docs = session.execute_write(_create_relationships)
                total_number_of_processed_functions += 1000
                logger.info(f"total number of processed functions:{total_number_of_processed_functions}")
            except Exception as e:
                error_message = f"Error occurred while retrieving total number of nodes: {e}"
                logger.error(error_message)
                raise Neo4jException(error_message)
        return total_number_of_processed_functions

    def create_index(self,logger:Logger):
        def inxed_on_uuid(tx):
            query = """
            CREATE CONSTRAINT code_block_index FOR (m:code_block) REQUIRE m.uuid IS UNIQUE
            """
            retuslts = tx.run(query)
            for result in retuslts:
                print(result)
            return retuslts
        try:
            with self.driver.session() as session:
                docs = session.execute_write(inxed_on_uuid)
            logger.info(f"Index is created successfully on the code_blocks")
            return True
        except Exception as e:
            error_message = f"Error occurred while indexing on code_blocks: {e}"
            logger.error(error_message)
            raise Neo4jException(error_message)
    
    def create_sematic_index(self,logger:Logger):
        def _create_sematic_index(tx):
            query = f"""
            CREATE VECTOR INDEX code_block_vector_index
            FOR (n: code_block) ON (n.embedding_large)
            OPTIONS {{indexConfig: {{
            `vector.dimensions`: 1536,
            `vector.similarity_function`: 'cosine'
            }}}};
            """
            docs = tx.run(query)
            return docs
        try:
            with self.driver.session() as session:
                docs = session.execute_write(_create_sematic_index)
            logger.info(f"Semantic index is created successfully on the code_blocks")
            return True
        except Exception as e:
            error_message = f"Error occurred while semantic indexing: {e}"
            logger.error(error_message)
            raise Neo4jException(error_message)

    def retrive_semantic_paths(self,embeddings,logger:Logger):
        def path_search(tx):
            query = f"""
            with {embeddings} as query_embedding
            CALL db.index.vector.queryNodes('code_block_vector_index', 100, query_embedding)
            YIELD node AS item, score
            WHERE item.node_type = 'code_block'
            MATCH path = (n)-[:child*]->(m)
            WHERE NOT (m)-[:child]->() and n.uuid = item.uuid
            with path, nodes(path) AS pathNodes, query_embedding, id(item) as item_id

            UNWIND range(0, size(pathNodes)-1) AS idx
            WITH pathNodes[idx] AS middleNode,idx,query_embedding,item_id

            WITH middleNode.content as content, gds.similarity.cosine(middleNode.embedding_large, query_embedding) AS similarity, idx,item_id
            RETURN item_id,idx,similarity, content
            """
            doc_info = []
            docs = tx.run(query)
            for doc in docs:
                print(doc)
                doc_info.append({'item_id':doc['item_id'],'idx':doc['idx'],'similarity':doc['similarity'],'content':doc['content']})
            return doc_info
        try:
            with self.driver.session() as session:
                docs = session.execute_read(path_search)
                logger.info(f"Successfully retrieved {len(docs)} nodes.")
                return docs
        except Exception as e:
            error_message = f"Error occurred while searching on semantic paths: {e}"
            logger.error(error_message)
            raise Neo4jException(error_message)
    
    def retrive_semantic_paths_old(self,embeddings,logger:Logger):
        def path_search(tx):
            query = f"""
            CALL db.index.vector.queryNodes('code_block_vector_index', 100, {embeddings})
            YIELD node AS item, score
            WHERE item.node_type = 'code_block' 
            RETURN score, item.content AS content, item.embedding as embedding
            """
            doc_info = []
            docs = tx.run(query)
            for doc in docs:
                print(doc)
                doc_info.append({'similarity':doc['score'],'content':doc['content']})
            return doc_info
        try:
            with self.driver.session() as session:
                docs = session.execute_read(path_search)
                logger.info(f"Successfully retrieved {len(docs)} nodes.")
                return docs
        except Exception as e:
            error_message = f"Error occurred while searching on semantic paths: {e}"
            logger.error(error_message)
            raise Neo4jException(error_message)
    
    def delete_all(self,logger:Logger):
        def _delete_all(tx):
            query = """
            MATCH (n) DETACH DELETE n
            """
            docs = tx.run(query)
            for doc in docs:
                print(doc['n'])
            return docs
        try:
            with self.driver.session() as session:
                docs = session.execute_write(_delete_all)
            logger.info(f"All nodes and relations are successfully deleted.")
            return True
        except Exception as e:
            error_message = f"Error occurred while deleting nodes and relations: {e}"
            logger.error(error_message)
            raise Neo4jException(error_message)   
    
    

