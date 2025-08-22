"""
Automatic Demo for Primal TCG Q&A System
Demonstrates all Q&A capabilities without user input
"""

import os
import sys
import time
from colorama import init, Fore, Style
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from loaders.document_loader import PrimalTCGDocumentLoader
from retrievers.vector_store import PrimalTCGVectorStore, SmartRetriever
from chains.qa_chain import PrimalTCGQAChain, ConversationalQAChain
from utils.formatters import ResponseFormatter

# Initialize colorama
init(autoreset=True)


def print_section(title: str, color=Fore.CYAN):
    """Print a formatted section header"""
    print(f"\n{color}{'='*70}")
    print(f"{color}{title.center(70)}")
    print(f"{color}{'='*70}\n")


def print_subsection(title: str):
    """Print a subsection header"""
    print(f"\n{Fore.YELLOW}➤ {title}")
    print(f"{Fore.YELLOW}{'-'*60}\n")


def pause(seconds: float = 2):
    """Pause for dramatic effect"""
    time.sleep(seconds)


class AutomaticQADemo:
    def __init__(self):
        print_section("🎮 PRIMAL TCG Q&A SYSTEM - AUTOMATIC DEMONSTRATION 🎮", Fore.MAGENTA)
        print(f"{Fore.WHITE}This demo showcases the RetrievalQA system from Lesson 4")
        print(f"{Fore.WHITE}Applied to Primal TCG for deck building assistance\n")
        pause(2)
        
        # Initialize components
        print(f"{Fore.YELLOW}Initializing Q&A System...")
        self.loader = PrimalTCGDocumentLoader()
        self.vector_store = PrimalTCGVectorStore(use_chroma=False)
        self.formatter = ResponseFormatter()
        
        # Load and process documents
        self._setup_system()
        
        print(f"{Fore.GREEN}✓ System initialized successfully\n")
        pause(1)
    
    def _setup_system(self):
        """Setup the Q&A system"""
        # Load documents
        print(f"{Fore.WHITE}Loading documents from multiple sources...")
        documents = self.loader.load_all_documents()
        print(f"  • Cards: {len(self.loader.cards_docs)}")
        print(f"  • Rules: {len(self.loader.rules_docs)} chunks")
        print(f"  • Decks: {len(self.loader.deck_docs)} documents")
        
        # Create vector store
        print(f"{Fore.WHITE}Creating vector store with embeddings...")
        self.vector_store.create_vectorstore(documents)
        
        # Initialize QA chains
        retriever = self.vector_store.get_retriever(search_kwargs={"k": 4})
        self.qa_chain = PrimalTCGQAChain(retriever, verbose=False)
        self.conversational_chain = ConversationalQAChain(retriever, verbose=False)
    
    def demo_1_basic_retrieval(self):
        """Demonstrate basic document retrieval and similarity search"""
        print_section("DEMO 1: Basic Document Retrieval", Fore.GREEN)
        print(f"{Fore.WHITE}Demonstrating similarity search with embeddings (from lesson)\n")
        
        query = "Show me cards with TRIGGER abilities"
        print(f"{Fore.CYAN}Query: {query}")
        print(f"{Fore.WHITE}Performing similarity search...\n")
        
        # Similarity search
        docs = self.vector_store.similarity_search(query, k=3)
        
        print(f"{Fore.GREEN}Top 3 Similar Documents:")
        for i, doc in enumerate(docs, 1):
            doc_type = doc.metadata.get('doc_type', 'unknown')
            print(f"\n{Fore.YELLOW}Document {i} ({doc_type}):")
            print(f"{Fore.WHITE}{doc.page_content[:200]}...")
        
        pause(3)
    
    def demo_2_qa_chain_types(self):
        """Demonstrate different QA chain types"""
        print_section("DEMO 2: RetrievalQA Chain Types", Fore.GREEN)
        print(f"{Fore.WHITE}Showing different chain types for various query types\n")
        
        test_cases = [
            {
                'type': 'Deck Building',
                'query': 'What cards work well with Synthetic Laboratory field card?',
                'chain_type': 'deck_building'
            },
            {
                'type': 'Card Search',
                'query': 'List all Fire element cards with cost 2 or less',
                'chain_type': 'card_search'
            },
            {
                'type': 'Rules Clarification',
                'query': 'How does TRIGGER ability timing work?',
                'chain_type': 'rules'
            },
            {
                'type': 'Comparison',
                'query': 'Compare TRIGGER vs ACTIVATE abilities for deck building',
                'chain_type': 'comparison'
            }
        ]
        
        for test in test_cases:
            print_subsection(f"{test['type']} Query")
            print(f"{Fore.CYAN}Question: {test['query']}")
            print(f"{Fore.YELLOW}Using chain type: {test['chain_type']}\n")
            
            result = self.qa_chain.query(test['query'], chain_type=test['chain_type'])
            
            print(f"{Fore.GREEN}Answer:")
            # Show first 400 chars of answer
            answer_preview = result['result'][:400] + "..." if len(result['result']) > 400 else result['result']
            print(f"{Fore.WHITE}{answer_preview}")
            
            if result.get('source_documents'):
                print(f"\n{Fore.YELLOW}Sources: {len(result['source_documents'])} documents retrieved")
            
            pause(2)
    
    def demo_3_retrieval_strategies(self):
        """Demonstrate different retrieval strategies"""
        print_section("DEMO 3: Advanced Retrieval Strategies", Fore.GREEN)
        print(f"{Fore.WHITE}Comparing similarity, MMR, and hybrid search\n")
        
        query = "Build a competitive Fire/Air aggro deck"
        print(f"{Fore.CYAN}Query: {query}\n")
        
        # 1. Similarity Search
        print_subsection("Similarity Search (Standard)")
        sim_docs = self.vector_store.similarity_search(query, k=3)
        print(f"{Fore.WHITE}Retrieved {len(sim_docs)} documents:")
        for doc in sim_docs:
            print(f"  • {doc.metadata.get('doc_type', 'unknown')}: {doc.page_content[:80]}...")
        
        # 2. MMR Search
        print_subsection("MMR Search (Maximum Marginal Relevance)")
        print(f"{Fore.WHITE}Balances relevance with diversity")
        mmr_docs = self.vector_store.mmr_search(query, k=3, lambda_mult=0.5)
        print(f"Retrieved {len(mmr_docs)} diverse documents:")
        for doc in mmr_docs:
            print(f"  • {doc.metadata.get('doc_type', 'unknown')}: {doc.page_content[:80]}...")
        
        # 3. Hybrid Search
        print_subsection("Hybrid Search (Multi-source)")
        print(f"{Fore.WHITE}Combines cards, rules, and deck documents")
        hybrid_docs = self.vector_store.hybrid_search(query, k=4)
        print(f"Retrieved {len(hybrid_docs)} documents from multiple sources:")
        for doc in hybrid_docs:
            print(f"  • {doc.metadata.get('doc_type', 'unknown')}: {doc.page_content[:80]}...")
        
        pause(3)
    
    def demo_4_conversational_qa(self):
        """Demonstrate conversational Q&A with memory"""
        print_section("DEMO 4: Conversational Q&A with Memory", Fore.GREEN)
        print(f"{Fore.WHITE}Multi-turn conversation for iterative deck building\n")
        
        conversation = [
            "I want to build a deck around TRIGGER abilities",
            "What elements work best with TRIGGER strategies?",
            "Can you suggest specific cards for a Fire TRIGGER deck?",
            "How many TRIGGER cards should I include in a 40-card deck?"
        ]
        
        print(f"{Fore.YELLOW}Starting deck building conversation...\n")
        
        for i, question in enumerate(conversation, 1):
            print(f"{Fore.CYAN}Turn {i} - User: {question}")
            
            result = self.conversational_chain.query(question)
            
            # Show abbreviated answer
            answer = result['answer'][:300] + "..." if len(result['answer']) > 300 else result['answer']
            print(f"{Fore.GREEN}Assistant: {answer}\n")
            
            pause(1.5)
        
        print(f"{Fore.YELLOW}Conversation maintains context across all turns!")
        pause(2)
    
    def demo_5_document_processing(self):
        """Show how documents are processed and chunked"""
        print_section("DEMO 5: Document Processing Strategy", Fore.GREEN)
        print(f"{Fore.WHITE}Showing how different data sources are processed\n")
        
        print_subsection("Document Processing Decisions")
        
        processing_info = [
            {
                'source': 'Cards (CSV)',
                'strategy': 'Individual documents with metadata',
                'reason': 'Each card needs to be searchable independently with filtering'
            },
            {
                'source': 'Rules (Markdown)',
                'strategy': 'Chunked with overlap',
                'reason': 'Rules need context, but are too long for single documents'
            },
            {
                'source': 'Decks (JSON)',
                'strategy': 'Overview + Details documents',
                'reason': 'Need both high-level composition and specific card lists'
            }
        ]
        
        for info in processing_info:
            print(f"{Fore.CYAN}{info['source']}:")
            print(f"{Fore.WHITE}  Strategy: {info['strategy']}")
            print(f"{Fore.YELLOW}  Rationale: {info['reason']}\n")
        
        # Show actual document examples
        print_subsection("Document Examples")
        
        # Card document
        card_doc = next((d for d in self.loader.cards_docs if 'TRIGGER' in d.page_content), None)
        if card_doc:
            print(f"{Fore.CYAN}Card Document:")
            print(f"{Fore.WHITE}{card_doc.page_content[:200]}...")
            print(f"{Fore.YELLOW}Metadata: {list(card_doc.metadata.keys())[:5]}...\n")
        
        # Rules document
        if self.loader.rules_docs:
            print(f"{Fore.CYAN}Rules Document Chunk:")
            print(f"{Fore.WHITE}{self.loader.rules_docs[0].page_content[:200]}...")
            print(f"{Fore.YELLOW}Metadata: {self.loader.rules_docs[0].metadata}\n")
        
        # Deck document
        if self.loader.deck_docs:
            print(f"{Fore.CYAN}Deck Overview Document:")
            print(f"{Fore.WHITE}{self.loader.deck_docs[0].page_content[:200]}...")
        
        pause(3)
    
    def demo_6_comprehensive_query(self):
        """Demonstrate a comprehensive deck building query"""
        print_section("DEMO 6: Comprehensive Deck Building Query", Fore.GREEN)
        print(f"{Fore.WHITE}Complex query using all system capabilities\n")
        
        query = """Build a competitive Synthetic Laboratory deck focusing on 
        Synthetic Life creatures with TRIGGER abilities. Include mana curve 
        recommendations and key synergies."""
        
        print(f"{Fore.CYAN}Complex Query:")
        print(f"{Fore.WHITE}{query}\n")
        
        print(f"{Fore.YELLOW}Processing with deck_building chain...\n")
        
        result = self.qa_chain.query(query, chain_type='deck_building')
        
        print(f"{Fore.GREEN}Comprehensive Answer:")
        print(f"{Fore.WHITE}{result['result'][:800]}...")
        
        if result.get('source_documents'):
            print(f"\n{Fore.YELLOW}Information synthesized from {len(result['source_documents'])} sources:")
            for i, doc in enumerate(result['source_documents'][:3], 1):
                doc_type = doc.metadata.get('doc_type', 'unknown')
                print(f"  {i}. {doc_type.title()} source")
        
        pause(3)
    
    def demo_7_performance_comparison(self):
        """Compare performance of different approaches"""
        print_section("DEMO 7: Approach Comparison", Fore.GREEN)
        print(f"{Fore.WHITE}Comparing basic vs advanced retrieval for deck building\n")
        
        query = "What are good Fire element cards for aggro?"
        
        print_subsection("Basic Approach (Lesson 4 Default)")
        print(f"{Fore.WHITE}Simple similarity search + basic QA chain")
        
        # Basic retriever
        basic_retriever = self.vector_store.get_retriever(
            search_type="similarity",
            search_kwargs={"k": 2}
        )
        basic_chain = PrimalTCGQAChain(basic_retriever, verbose=False)
        
        start_time = time.time()
        basic_result = basic_chain.query(query, chain_type='general')
        basic_time = time.time() - start_time
        
        print(f"Time: {basic_time:.2f}s")
        print(f"Answer preview: {basic_result['result'][:150]}...")
        
        print_subsection("Advanced Approach (Our Implementation)")
        print(f"{Fore.WHITE}Smart retrieval + specialized chain + custom prompts")
        
        start_time = time.time()
        advanced_result = self.qa_chain.query(query, chain_type='deck_building')
        advanced_time = time.time() - start_time
        
        print(f"Time: {advanced_time:.2f}s")
        print(f"Answer preview: {advanced_result['result'][:150]}...")
        
        print(f"\n{Fore.GREEN}Advanced approach provides more detailed, deck-focused answers!")
        pause(2)
    
    def run_summary(self):
        """Summarize the demonstration"""
        print_section("DEMONSTRATION COMPLETE", Fore.MAGENTA)
        
        print(f"{Fore.WHITE}We've demonstrated a comprehensive Q&A system for Primal TCG that:")
        print(f"{Fore.WHITE}extends the concepts from Lesson 4: Q&A over Documents\n")
        
        print(f"{Fore.CYAN}Key Features Demonstrated:")
        print(f"{Fore.WHITE}1. Multi-source document loading (CSV, Markdown, JSON)")
        print(f"{Fore.WHITE}2. Smart document processing strategies")
        print(f"{Fore.WHITE}3. Multiple retrieval strategies (similarity, MMR, hybrid)")
        print(f"{Fore.WHITE}4. Specialized QA chains for different query types")
        print(f"{Fore.WHITE}5. Conversational Q&A with memory")
        print(f"{Fore.WHITE}6. Custom prompts for deck building focus\n")
        
        print(f"{Fore.GREEN}Advantages Over Basic Implementation:")
        print(f"{Fore.WHITE}• Better context preservation through smart chunking")
        print(f"{Fore.WHITE}• More relevant results with metadata filtering")
        print(f"{Fore.WHITE}• Specialized chains for different user intents")
        print(f"{Fore.WHITE}• Conversational capability for iterative refinement\n")
        
        print(f"{Fore.YELLOW}Perfect for:")
        print(f"{Fore.WHITE}• Deck building assistance")
        print(f"{Fore.WHITE}• Rules clarification")
        print(f"{Fore.WHITE}• Card discovery")
        print(f"{Fore.WHITE}• Strategy development\n")
        
        print(f"{Fore.MAGENTA}{'='*70}")
        print(f"{Fore.MAGENTA}Thank you for watching the Primal TCG Q&A demonstration!")
        print(f"{Fore.MAGENTA}{'='*70}")
    
    def run(self):
        """Run the complete automatic demonstration"""
        try:
            print(f"{Fore.YELLOW}Starting automatic demonstration...\n")
            pause(2)
            
            # Run each demo
            self.demo_1_basic_retrieval()
            pause(2)
            
            self.demo_2_qa_chain_types()
            pause(2)
            
            self.demo_3_retrieval_strategies()
            pause(2)
            
            self.demo_4_conversational_qa()
            pause(2)
            
            self.demo_5_document_processing()
            pause(2)
            
            self.demo_6_comprehensive_query()
            pause(2)
            
            self.demo_7_performance_comparison()
            pause(2)
            
            self.run_summary()
            
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Demo interrupted by user.")
        except Exception as e:
            print(f"\n{Fore.RED}Error during demonstration: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print(f"{Fore.RED}Error: OPENAI_API_KEY not found in environment variables.")
        print(f"{Fore.YELLOW}Please set your OpenAI API key in the .env file.")
        sys.exit(1)
    
    # Run the automatic demo
    demo = AutomaticQADemo()
    demo.run()