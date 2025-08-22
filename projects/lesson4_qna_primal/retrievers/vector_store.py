"""
Vector Store and Retrieval System for Primal TCG Q&A
Implements multiple retrieval strategies: similarity, MMR, threshold
"""

from typing import List, Dict, Any, Optional
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import DocArrayInMemorySearch, Chroma
from langchain.schema import Document
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_openai import ChatOpenAI
import os


class PrimalTCGVectorStore:
    """
    Advanced vector store with multiple retrieval strategies.
    Optimized for deck building assistance queries.
    """
    
    def __init__(self, use_chroma: bool = False, persist_directory: str = None):
        """
        Initialize vector store.
        
        Args:
            use_chroma: Use Chroma for persistence instead of in-memory
            persist_directory: Directory for Chroma persistence
        """
        self.embeddings = OpenAIEmbeddings()
        self.use_chroma = use_chroma
        self.persist_directory = persist_directory
        self.vectorstore = None
        self.documents = []
        
    def create_vectorstore(self, documents: List[Document]) -> None:
        """Create vector store from documents"""
        self.documents = documents
        
        if self.use_chroma and self.persist_directory:
            # Use Chroma for persistence
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            print(f"Created Chroma vector store with {len(documents)} documents")
        else:
            # Use in-memory store (like the lesson)
            self.vectorstore = DocArrayInMemorySearch.from_documents(
                documents=documents,
                embedding=self.embeddings
            )
            print(f"Created in-memory vector store with {len(documents)} documents")
    
    def similarity_search(self, 
                         query: str, 
                         k: int = 4,
                         filter: Optional[Dict] = None) -> List[Document]:
        """
        Basic similarity search.
        
        Args:
            query: Search query
            k: Number of results
            filter: Metadata filter (e.g., {'doc_type': 'card'})
        """
        if not self.vectorstore:
            raise ValueError("Vector store not initialized. Call create_vectorstore first.")
        
        if filter and self.use_chroma:
            # Chroma supports metadata filtering
            return self.vectorstore.similarity_search(
                query=query,
                k=k,
                filter=filter
            )
        else:
            # For in-memory, we need to filter manually
            results = self.vectorstore.similarity_search(query=query, k=k*2)
            if filter:
                filtered = []
                for doc in results:
                    match = True
                    for key, value in filter.items():
                        if doc.metadata.get(key) != value:
                            match = False
                            break
                    if match:
                        filtered.append(doc)
                return filtered[:k]
            return results[:k]
    
    def mmr_search(self,
                   query: str,
                   k: int = 4,
                   fetch_k: int = 20,
                   lambda_mult: float = 0.5) -> List[Document]:
        """
        Maximum Marginal Relevance search for diverse results.
        Good for getting varied deck building options.
        
        Args:
            query: Search query
            k: Number of results to return
            fetch_k: Number of documents to fetch before MMR
            lambda_mult: Balance between relevance and diversity (0=max diversity, 1=max relevance)
        """
        if not self.vectorstore:
            raise ValueError("Vector store not initialized. Call create_vectorstore first.")
        
        return self.vectorstore.max_marginal_relevance_search(
            query=query,
            k=k,
            fetch_k=fetch_k,
            lambda_mult=lambda_mult
        )
    
    def threshold_search(self,
                        query: str,
                        score_threshold: float = 0.8,
                        k: int = 10) -> List[Document]:
        """
        Similarity search with score threshold.
        Only returns results above a certain similarity score.
        """
        if not self.vectorstore:
            raise ValueError("Vector store not initialized. Call create_vectorstore first.")
        
        # Get results with scores
        results_with_scores = self.vectorstore.similarity_search_with_score(
            query=query,
            k=k
        )
        
        # Filter by threshold
        filtered_results = []
        for doc, score in results_with_scores:
            # Note: Score interpretation depends on distance metric
            # For cosine similarity, higher is better (closer to 1)
            # For euclidean distance, lower is better (closer to 0)
            # DocArrayInMemorySearch uses cosine by default
            if score >= score_threshold:
                doc.metadata['similarity_score'] = score
                filtered_results.append(doc)
        
        return filtered_results
    
    def get_retriever(self, 
                      search_type: str = "similarity",
                      search_kwargs: Optional[Dict] = None):
        """
        Get a retriever with specified search type.
        
        Args:
            search_type: One of "similarity", "mmr", "similarity_score_threshold"
            search_kwargs: Additional search parameters
        """
        if not self.vectorstore:
            raise ValueError("Vector store not initialized. Call create_vectorstore first.")
        
        if search_kwargs is None:
            search_kwargs = {"k": 4}
        
        return self.vectorstore.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs
        )
    
    def get_contextual_compression_retriever(self, 
                                            base_retriever=None,
                                            llm=None):
        """
        Get a retriever with contextual compression.
        This extracts only relevant parts of documents.
        Useful for long documents like rules.
        """
        if not base_retriever:
            base_retriever = self.get_retriever()
        
        if not llm:
            llm = ChatOpenAI(temperature=0)
        
        compressor = LLMChainExtractor.from_llm(llm)
        
        return ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=base_retriever
        )
    
    def hybrid_search(self,
                     query: str,
                     card_weight: float = 0.4,
                     rules_weight: float = 0.3,
                     deck_weight: float = 0.3,
                     k: int = 6) -> List[Document]:
        """
        Hybrid search across different document types with weighting.
        Optimized for deck building queries.
        """
        results = []
        
        # Search cards
        if card_weight > 0:
            card_results = self.similarity_search(
                query=query,
                k=int(k * card_weight),
                filter={'doc_type': 'card'}
            )
            results.extend(card_results)
        
        # Search rules
        if rules_weight > 0:
            rules_results = self.similarity_search(
                query=query,
                k=int(k * rules_weight),
                filter={'doc_type': 'rules'}
            )
            results.extend(rules_results)
        
        # Search decks
        if deck_weight > 0:
            deck_results = self.similarity_search(
                query=query,
                k=int(k * deck_weight),
                filter={'source': 'deck'}
            )
            results.extend(deck_results)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_results = []
        for doc in results:
            doc_id = doc.page_content[:100]  # Use first 100 chars as ID
            if doc_id not in seen:
                seen.add(doc_id)
                unique_results.append(doc)
        
        return unique_results[:k]


class SmartRetriever:
    """
    Smart retriever that chooses the best retrieval strategy based on query type.
    """
    
    def __init__(self, vector_store: PrimalTCGVectorStore):
        self.vector_store = vector_store
        self.llm = ChatOpenAI(temperature=0)
        
    def detect_query_type(self, query: str) -> str:
        """
        Detect the type of query to choose appropriate retrieval strategy.
        """
        query_lower = query.lower()
        
        # Deck building queries
        if any(word in query_lower for word in ['deck', 'build', 'synergy', 'combo', 'works with']):
            return 'deck_building'
        
        # Card search queries
        if any(word in query_lower for word in ['card', 'cards', 'show', 'list', 'find', 'search']):
            return 'card_search'
        
        # Rules queries
        if any(word in query_lower for word in ['rule', 'how', 'when', 'trigger', 'phase', 'can i', 'legal']):
            return 'rules'
        
        # Comparison queries
        if any(word in query_lower for word in ['compare', 'versus', 'vs', 'better', 'difference']):
            return 'comparison'
        
        return 'general'
    
    def retrieve(self, query: str, k: int = 4) -> List[Document]:
        """
        Smart retrieval based on query type.
        """
        query_type = self.detect_query_type(query)
        
        if query_type == 'deck_building':
            # Use MMR for diverse suggestions
            return self.vector_store.mmr_search(
                query=query,
                k=k,
                lambda_mult=0.7  # Balance relevance and diversity
            )
        
        elif query_type == 'card_search':
            # Use similarity search with card filter
            return self.vector_store.similarity_search(
                query=query,
                k=k,
                filter={'doc_type': 'card'}
            )
        
        elif query_type == 'rules':
            # Use similarity search with rules filter
            return self.vector_store.similarity_search(
                query=query,
                k=k,
                filter={'doc_type': 'rules'}
            )
        
        elif query_type == 'comparison':
            # Use MMR for diverse perspectives
            return self.vector_store.mmr_search(
                query=query,
                k=k,
                lambda_mult=0.5  # More diversity for comparisons
            )
        
        else:
            # Use hybrid search for general queries
            return self.vector_store.hybrid_search(
                query=query,
                k=k
            )