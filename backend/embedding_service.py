import os 
import voyageai
from logging import Logger

class EmbeddingException(Exception):
    def __init__(self, message):
        super().__init__(message)

class EmbeddingService:
    def __init__(self):
        voyageai.api_key = os.getenv("VOYAGE_API_KEY","pa-lpHvggxAmQX_QTSipVOhn7qC5Ue_9XRxT_RGwCEFRmE")
        self.model_name = os.getenv("EMBEDDER_MODEL","voyage-code-2")
        self.embedder = voyageai.Client()
    
    def get_embeddings(self,strings,logger:Logger):
        if not isinstance(strings, list) or not all(isinstance(s, str) for s in strings):
            raise TypeError("Input must be a list of strings")
        try:
            query_embedding = self.embedder.embed(strings, model="voyage-code-2").embeddings
            logger.info(f"Embeddings retrieved succussfully.")
            return query_embedding
        except Exception as e:
            error_message = f"Error occurred while getting embeddings from embedder model: {e}"
            logger.error(error_message)
            raise EmbeddingException(error_message)