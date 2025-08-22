"""
Interactive Demo for Primal TCG Q&A System
Demonstrates RetrievalQA with multiple retrieval strategies
"""

import os
import sys
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


class InteractiveQADemo:
    def __init__(self):
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}🎮 Primal TCG Q&A System - Interactive Demo")
        print(f"{Fore.CYAN}{'='*60}\n")
        
        # Initialize components
        self.loader = None
        self.vector_store = None
        self.qa_chain = None
        self.conversational_chain = None
        self.formatter = ResponseFormatter()
        self.documents = []
        
        # Initialize system
        self._initialize_system()
    
    def _initialize_system(self):
        """Initialize the Q&A system components"""
        print(f"{Fore.YELLOW}Initializing Q&A System...")
        
        # Load documents
        print(f"{Fore.WHITE}Loading documents...")
        self.loader = PrimalTCGDocumentLoader()
        self.documents = self.loader.load_all_documents()
        print(f"{Fore.GREEN}✓ Loaded {len(self.documents)} documents")
        
        # Create vector store
        print(f"{Fore.WHITE}Creating vector store...")
        self.vector_store = PrimalTCGVectorStore(use_chroma=False)
        self.vector_store.create_vectorstore(self.documents)
        print(f"{Fore.GREEN}✓ Vector store ready")
        
        # Initialize QA chains
        print(f"{Fore.WHITE}Initializing QA chains...")
        retriever = self.vector_store.get_retriever(search_kwargs={"k": 4})
        self.qa_chain = PrimalTCGQAChain(retriever, verbose=False)
        self.conversational_chain = ConversationalQAChain(retriever, verbose=False)
        print(f"{Fore.GREEN}✓ QA chains ready\n")
    
    def display_menu(self):
        """Display the main menu"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}MAIN MENU - Choose Query Type:")
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.WHITE}1. {Fore.GREEN}Deck Building Assistance{Fore.WHITE} - Get help building decks")
        print(f"{Fore.WHITE}2. {Fore.GREEN}Card Search{Fore.WHITE} - Find specific cards")
        print(f"{Fore.WHITE}3. {Fore.GREEN}Rules Clarification{Fore.WHITE} - Get rules explanations")
        print(f"{Fore.WHITE}4. {Fore.GREEN}Card Comparison{Fore.WHITE} - Compare cards or strategies")
        print(f"{Fore.WHITE}5. {Fore.GREEN}Free Query{Fore.WHITE} - Ask anything (auto-detect type)")
        print(f"{Fore.WHITE}6. {Fore.GREEN}Conversational Mode{Fore.WHITE} - Multi-turn deck building session")
        print(f"{Fore.WHITE}7. {Fore.YELLOW}Test Retrieval Strategies{Fore.WHITE} - Compare different retrievers")
        print(f"{Fore.WHITE}8. {Fore.YELLOW}View Sample Queries{Fore.WHITE} - See example questions")
        print(f"{Fore.WHITE}0. {Fore.RED}Exit")
        print(f"{Fore.CYAN}{'='*60}")
    
    def deck_building_mode(self):
        """Deck building assistance mode"""
        print(f"\n{Fore.GREEN}DECK BUILDING ASSISTANCE MODE")
        print(f"{Fore.WHITE}Ask about synergies, combos, or deck composition.\n")
        
        sample_queries = [
            "What cards work well with Synthetic Laboratory?",
            "Build a Fire/Air aggro deck",
            "What are good TRIGGER synergies?",
            "Suggest cards for a BIO attribute deck"
        ]
        
        print(f"{Fore.YELLOW}Sample queries:")
        for q in sample_queries:
            print(f"  - {q}")
        
        query = input(f"\n{Fore.CYAN}Your deck building question: ").strip()
        if not query:
            return
        
        print(f"\n{Fore.YELLOW}Searching for deck building advice...")
        result = self.qa_chain.query(query, chain_type='deck_building')
        
        print(f"\n{Fore.GREEN}Answer:")
        print(f"{Fore.WHITE}{result['result']}")
        
        if result.get('source_documents'):
            print(f"\n{Fore.YELLOW}Based on {len(result['source_documents'])} sources")
    
    def card_search_mode(self):
        """Card search mode"""
        print(f"\n{Fore.GREEN}CARD SEARCH MODE")
        print(f"{Fore.WHITE}Search for specific cards or card types.\n")
        
        sample_queries = [
            "Show me all Fire element cards with cost 2 or less",
            "List all TRIGGER abilities",
            "Find cards with REBIRTH",
            "Show all Synthetic Life creatures"
        ]
        
        print(f"{Fore.YELLOW}Sample queries:")
        for q in sample_queries:
            print(f"  - {q}")
        
        query = input(f"\n{Fore.CYAN}Your card search: ").strip()
        if not query:
            return
        
        print(f"\n{Fore.YELLOW}Searching cards...")
        result = self.qa_chain.query(query, chain_type='card_search')
        
        print(f"\n{Fore.GREEN}Results:")
        print(f"{Fore.WHITE}{result['result']}")
    
    def rules_mode(self):
        """Rules clarification mode"""
        print(f"\n{Fore.GREEN}RULES CLARIFICATION MODE")
        print(f"{Fore.WHITE}Ask about game rules and mechanics.\n")
        
        sample_queries = [
            "How does TRIGGER stacking work?",
            "When can I activate abilities?",
            "Explain the combat phase",
            "What is REBIRTH?"
        ]
        
        print(f"{Fore.YELLOW}Sample queries:")
        for q in sample_queries:
            print(f"  - {q}")
        
        query = input(f"\n{Fore.CYAN}Your rules question: ").strip()
        if not query:
            return
        
        print(f"\n{Fore.YELLOW}Looking up rules...")
        result = self.qa_chain.query(query, chain_type='rules')
        
        print(f"\n{Fore.GREEN}Rules Clarification:")
        print(f"{Fore.WHITE}{result['result']}")
    
    def comparison_mode(self):
        """Card/strategy comparison mode"""
        print(f"\n{Fore.GREEN}COMPARISON MODE")
        print(f"{Fore.WHITE}Compare cards, strategies, or deck types.\n")
        
        sample_queries = [
            "Compare Fire vs Air elements for aggro",
            "Which is better: TRIGGER or ACTIVATE abilities?",
            "Compare BIO vs PLEAGUIS attributes",
            "Synthetic Life vs Zoltan creatures"
        ]
        
        print(f"{Fore.YELLOW}Sample queries:")
        for q in sample_queries:
            print(f"  - {q}")
        
        query = input(f"\n{Fore.CYAN}What would you like to compare? ").strip()
        if not query:
            return
        
        print(f"\n{Fore.YELLOW}Analyzing comparison...")
        result = self.qa_chain.query(query, chain_type='comparison')
        
        print(f"\n{Fore.GREEN}Comparison:")
        print(f"{Fore.WHITE}{result['result']}")
    
    def free_query_mode(self):
        """Free query with auto-detection"""
        print(f"\n{Fore.GREEN}FREE QUERY MODE")
        print(f"{Fore.WHITE}Ask anything - the system will detect the query type.\n")
        
        query = input(f"{Fore.CYAN}Your question: ").strip()
        if not query:
            return
        
        # Detect and display query type
        query_type = self.qa_chain.detect_query_type(query)
        print(f"\n{Fore.YELLOW}Detected query type: {query_type}")
        print(f"{Fore.YELLOW}Processing...")
        
        result = self.qa_chain.query(query)
        
        print(f"\n{Fore.GREEN}Answer:")
        print(f"{Fore.WHITE}{result['result']}")
        
        if result.get('source_documents'):
            print(f"\n{Fore.YELLOW}Sources used: {len(result['source_documents'])}")
    
    def conversational_mode(self):
        """Multi-turn conversational mode"""
        print(f"\n{Fore.GREEN}CONVERSATIONAL MODE")
        print(f"{Fore.WHITE}Have a conversation about deck building. Type 'clear' to reset or 'exit' to leave.\n")
        
        while True:
            query = input(f"\n{Fore.CYAN}You: ").strip()
            
            if query.lower() == 'exit':
                break
            elif query.lower() == 'clear':
                self.conversational_chain.clear_memory()
                print(f"{Fore.YELLOW}Conversation memory cleared.")
                continue
            elif not query:
                continue
            
            print(f"\n{Fore.YELLOW}Thinking...")
            result = self.conversational_chain.query(query)
            
            print(f"\n{Fore.GREEN}Assistant:")
            print(f"{Fore.WHITE}{result['answer']}")
    
    def test_retrieval_strategies(self):
        """Test different retrieval strategies"""
        print(f"\n{Fore.GREEN}RETRIEVAL STRATEGY TESTING")
        print(f"{Fore.WHITE}Compare different retrieval methods.\n")
        
        query = input(f"{Fore.CYAN}Enter test query: ").strip()
        if not query:
            return
        
        print(f"\n{Fore.YELLOW}Testing retrieval strategies...\n")
        
        # Test similarity search
        print(f"{Fore.CYAN}1. Similarity Search (k=4):")
        sim_docs = self.vector_store.similarity_search(query, k=4)
        for i, doc in enumerate(sim_docs, 1):
            doc_type = doc.metadata.get('doc_type', 'unknown')
            print(f"  {i}. {doc_type}: {doc.page_content[:100]}...")
        
        # Test MMR search
        print(f"\n{Fore.CYAN}2. MMR Search (diversity-focused):")
        mmr_docs = self.vector_store.mmr_search(query, k=4, lambda_mult=0.5)
        for i, doc in enumerate(mmr_docs, 1):
            doc_type = doc.metadata.get('doc_type', 'unknown')
            print(f"  {i}. {doc_type}: {doc.page_content[:100]}...")
        
        # Test hybrid search
        print(f"\n{Fore.CYAN}3. Hybrid Search (cards+rules+decks):")
        hybrid_docs = self.vector_store.hybrid_search(query, k=6)
        for i, doc in enumerate(hybrid_docs, 1):
            doc_type = doc.metadata.get('doc_type', 'unknown')
            print(f"  {i}. {doc_type}: {doc.page_content[:100]}...")
    
    def show_sample_queries(self):
        """Display sample queries for each category"""
        print(f"\n{Fore.GREEN}SAMPLE QUERIES")
        
        categories = {
            "Deck Building": [
                "What cards synergize with TRIGGER abilities?",
                "Build a competitive Fire/Air deck",
                "What are the best cards for a BIO attribute strategy?",
                "How do I build around Synthetic Laboratory?"
            ],
            "Card Search": [
                "Show all cards with REBIRTH",
                "List Fire element cards under 3 cost",
                "Find all Synthetic Life creatures",
                "What cards have ACTIVATE abilities?"
            ],
            "Rules": [
                "How does combat work?",
                "When do TRIGGER abilities activate?",
                "What is the difference between Leader and Support values?",
                "Can I activate abilities during my opponent's turn?"
            ],
            "Comparison": [
                "Compare TRIGGER vs ACTIVATE abilities",
                "Which is better for aggro: Fire or Air?",
                "Compare BIO vs PLEAGUIS strategies",
                "Synthetic Life vs Zoltan: which is stronger?"
            ]
        }
        
        for category, queries in categories.items():
            print(f"\n{Fore.CYAN}{category}:")
            for q in queries:
                print(f"{Fore.WHITE}  • {q}")
    
    def run(self):
        """Main demo loop"""
        while True:
            self.display_menu()
            
            choice = input(f"\n{Fore.CYAN}Enter your choice (0-8): ").strip()
            
            if choice == "0":
                print(f"\n{Fore.YELLOW}Thank you for using Primal TCG Q&A System!")
                print(f"{Fore.GREEN}May your queries always find answers! 🎮")
                break
            elif choice == "1":
                self.deck_building_mode()
            elif choice == "2":
                self.card_search_mode()
            elif choice == "3":
                self.rules_mode()
            elif choice == "4":
                self.comparison_mode()
            elif choice == "5":
                self.free_query_mode()
            elif choice == "6":
                self.conversational_mode()
            elif choice == "7":
                self.test_retrieval_strategies()
            elif choice == "8":
                self.show_sample_queries()
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.")
            
            if choice in ["1", "2", "3", "4", "5", "7"]:
                input(f"\n{Fore.YELLOW}Press Enter to continue...")


if __name__ == "__main__":
    try:
        # Check for API key
        if not os.getenv("OPENAI_API_KEY"):
            print(f"{Fore.RED}Error: OPENAI_API_KEY not found in environment variables.")
            print(f"{Fore.YELLOW}Please set your OpenAI API key in the .env file.")
            sys.exit(1)
        
        demo = InteractiveQADemo()
        demo.run()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Demo interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)