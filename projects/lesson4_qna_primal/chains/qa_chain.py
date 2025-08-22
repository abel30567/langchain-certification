"""
RetrievalQA Chain for Primal TCG Q&A System
Implements various chain types for different query types
"""

from typing import List, Dict, Any, Optional
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.callbacks import StdOutCallbackHandler
from langchain.memory import ConversationBufferMemory


class PrimalTCGQAChain:
    """
    Advanced Q&A chain system for Primal TCG queries.
    Supports multiple chain types and custom prompts for deck building.
    """
    
    def __init__(self, retriever, llm=None, verbose: bool = False):
        """
        Initialize QA chain.
        
        Args:
            retriever: Langchain retriever
            llm: Language model (defaults to ChatOpenAI)
            verbose: Enable verbose output
        """
        self.retriever = retriever
        self.llm = llm or ChatOpenAI(temperature=0.3, model="gpt-3.5-turbo")
        self.verbose = verbose
        
        # Initialize different chain types
        self.chains = {}
        self._initialize_chains()
        
    def _initialize_chains(self):
        """Initialize different chain types with custom prompts"""
        
        # Deck Building Chain
        deck_building_prompt = PromptTemplate(
            template="""You are a Primal TCG deck building expert. Use the following pieces of context to answer the deck building question.
Focus on card synergies, mana curves, and competitive viability.

Context:
{context}

Question: {question}

Provide a detailed answer with:
1. Specific card recommendations (in a markdown table if multiple cards)
2. Synergy explanations
3. Deck building strategy
4. Any important rules interactions

Answer:""",
            input_variables=["context", "question"]
        )
        
        self.chains['deck_building'] = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            chain_type_kwargs={"prompt": deck_building_prompt},
            verbose=self.verbose,
            return_source_documents=True
        )
        
        # Card Search Chain
        card_search_prompt = PromptTemplate(
            template="""You are a Primal TCG card database assistant. Use the following card information to answer the query.
Format card lists as markdown tables when showing multiple cards.

Context:
{context}

Question: {question}

Format the response as follows:
1. If showing multiple cards, use a markdown table with columns: Name | Type | Cost | Effect | Rarity
2. Group cards by relevant categories (element, cost, etc.)
3. Highlight key cards with brief explanations

Answer:""",
            input_variables=["context", "question"]
        )
        
        self.chains['card_search'] = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            chain_type_kwargs={"prompt": card_search_prompt},
            verbose=self.verbose,
            return_source_documents=True
        )
        
        # Rules Clarification Chain
        rules_prompt = PromptTemplate(
            template="""You are a Primal TCG rules judge. Use the following rules context to provide accurate rulings.
Be precise and cite specific rule sections when possible.

Context:
{context}

Question: {question}

Provide:
1. Clear answer to the rules question
2. Relevant rule citations
3. Examples if helpful
4. Common misconceptions if applicable

Answer:""",
            input_variables=["context", "question"]
        )
        
        self.chains['rules'] = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            chain_type_kwargs={"prompt": rules_prompt},
            verbose=self.verbose,
            return_source_documents=True
        )
        
        # General/Default Chain
        general_prompt = PromptTemplate(
            template="""You are a helpful Primal TCG assistant. Use the following context to answer the question.
If the question involves cards, format them clearly. If it's about rules, be precise.

Context:
{context}

Question: {question}

Answer:""",
            input_variables=["context", "question"]
        )
        
        self.chains['general'] = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            chain_type_kwargs={"prompt": general_prompt},
            verbose=self.verbose,
            return_source_documents=True
        )
        
        # Comparison Chain
        comparison_prompt = PromptTemplate(
            template="""You are a Primal TCG analyst. Compare and contrast the items in question using the context provided.
Use tables or structured formats for clear comparison.

Context:
{context}

Question: {question}

Provide:
1. Clear comparison table if applicable
2. Pros and cons of each option
3. Situational recommendations
4. Overall verdict

Answer:""",
            input_variables=["context", "question"]
        )
        
        self.chains['comparison'] = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            chain_type_kwargs={"prompt": comparison_prompt},
            verbose=self.verbose,
            return_source_documents=True
        )
    
    def detect_query_type(self, query: str) -> str:
        """Detect query type to route to appropriate chain"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['deck', 'build', 'synergy', 'combo', 'works with']):
            return 'deck_building'
        elif any(word in query_lower for word in ['show', 'list', 'find', 'search', 'all cards']):
            return 'card_search'
        elif any(word in query_lower for word in ['rule', 'how', 'when', 'trigger', 'phase', 'can i']):
            return 'rules'
        elif any(word in query_lower for word in ['compare', 'versus', 'vs', 'better', 'difference']):
            return 'comparison'
        else:
            return 'general'
    
    def query(self, question: str, chain_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute a query using the appropriate chain.
        
        Args:
            question: The user's question
            chain_type: Optional chain type override
            
        Returns:
            Dictionary with 'result' and 'source_documents'
        """
        # Detect chain type if not specified
        if not chain_type:
            chain_type = self.detect_query_type(question)
        
        # Get the appropriate chain
        chain = self.chains.get(chain_type, self.chains['general'])
        
        # Execute query
        result = chain({"query": question})
        
        # Add metadata about chain type used
        result['chain_type'] = chain_type
        
        return result
    
    def format_response(self, result: Dict[str, Any]) -> str:
        """
        Format the response for display.
        
        Args:
            result: Query result dictionary
            
        Returns:
            Formatted string response
        """
        response = f"**Answer:**\n{result['result']}\n\n"
        
        if 'source_documents' in result and result['source_documents']:
            response += "**Sources:**\n"
            for i, doc in enumerate(result['source_documents'][:3], 1):
                source_type = doc.metadata.get('doc_type', 'unknown')
                if source_type == 'card':
                    card_name = doc.page_content.split('\n')[0].replace('Card Name: ', '')
                    response += f"{i}. Card: {card_name}\n"
                elif source_type == 'rules':
                    response += f"{i}. Rules Section {doc.metadata.get('section_index', 'N/A')}\n"
                elif source_type == 'deck_overview':
                    response += f"{i}. Deck: {doc.metadata.get('deck_name', 'Unknown')}\n"
                else:
                    response += f"{i}. {source_type.title()}\n"
        
        return response


class ConversationalQAChain:
    """
    Conversational Q&A chain with memory for multi-turn interactions.
    Useful for iterative deck building sessions.
    """
    
    def __init__(self, retriever, llm=None, verbose: bool = False):
        """Initialize conversational chain with memory"""
        self.retriever = retriever
        self.llm = llm or ChatOpenAI(temperature=0.3, model="gpt-3.5-turbo")
        self.verbose = verbose
        
        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        # Create conversational chain
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            verbose=self.verbose,
            return_source_documents=True
        )
    
    def query(self, question: str) -> Dict[str, Any]:
        """Execute a conversational query"""
        result = self.chain({"question": question})
        return result
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear()
    
    def get_conversation_history(self) -> List[tuple]:
        """Get the conversation history"""
        return self.memory.chat_memory.messages