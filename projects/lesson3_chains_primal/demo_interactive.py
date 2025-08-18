"""
Interactive Demo for Primal TCG Chains
Demonstrates all chain types with user interaction
"""

import os
import sys
from colorama import init, Fore, Style
from utils.data_loader import DeckLoader
from chains.deck_builder_chain import DeckBuilderChain
from chains.strategy_chain import StrategyAnalysisChain
from chains.router_chain import PrimalTCGRouterChain
from chains.competitive_chain import CompetitiveAnalysisChain

# Initialize colorama for colored output
init(autoreset=True)


class InteractiveDemo:
    def __init__(self):
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}🎮 Primal TCG Chain Analysis System")
        print(f"{Fore.CYAN}{'='*60}\n")
        
        # Initialize data loader
        print(f"{Fore.YELLOW}Loading deck data...")
        self.deck_loader = DeckLoader()
        self.available_decks = self.deck_loader.get_all_deck_names()
        print(f"{Fore.GREEN}✓ Loaded {len(self.available_decks)} decks\n")
        
        # Initialize chains
        print(f"{Fore.YELLOW}Initializing chain systems...")
        self.deck_builder = DeckBuilderChain()
        self.strategy_analyzer = StrategyAnalysisChain()
        self.router = PrimalTCGRouterChain()
        self.competitive_analyzer = CompetitiveAnalysisChain()
        print(f"{Fore.GREEN}✓ All systems ready\n")
        
        # Set verbosity
        self.verbose = True
    
    def display_menu(self):
        """Display the main menu"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}MAIN MENU - Choose a Chain Demo:")
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.WHITE}1. {Fore.GREEN}Simple Sequential Chain{Fore.WHITE} - Basic deck analysis")
        print(f"{Fore.WHITE}2. {Fore.GREEN}Complex Sequential Chain{Fore.WHITE} - Full deck optimization")
        print(f"{Fore.WHITE}3. {Fore.GREEN}Strategy Analysis Chain{Fore.WHITE} - Combo and game plan analysis")
        print(f"{Fore.WHITE}4. {Fore.GREEN}Router Chain{Fore.WHITE} - Ask any Primal TCG question")
        print(f"{Fore.WHITE}5. {Fore.GREEN}Competitive Analysis{Fore.WHITE} - Tournament-level analysis")
        print(f"{Fore.WHITE}6. {Fore.GREEN}Compare Decks{Fore.WHITE} - Head-to-head comparison")
        print(f"{Fore.WHITE}7. {Fore.GREEN}Deck Statistics{Fore.WHITE} - View deck composition")
        print(f"{Fore.WHITE}8. {Fore.YELLOW}Toggle Verbosity{Fore.WHITE} - Currently: {self.verbose}")
        print(f"{Fore.WHITE}0. {Fore.RED}Exit")
        print(f"{Fore.CYAN}{'='*60}")
    
    def select_deck(self) -> str:
        """Let user select a deck"""
        print(f"\n{Fore.YELLOW}Available decks:")
        for i, deck in enumerate(self.available_decks, 1):
            print(f"  {i}. {deck}")
        
        while True:
            try:
                choice = int(input(f"\n{Fore.CYAN}Select deck (1-{len(self.available_decks)}): "))
                if 1 <= choice <= len(self.available_decks):
                    return self.available_decks[choice - 1]
                print(f"{Fore.RED}Invalid choice. Please try again.")
            except ValueError:
                print(f"{Fore.RED}Please enter a number.")
    
    def demo_simple_sequential(self):
        """Demo 1: Simple Sequential Chain"""
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}SIMPLE SEQUENTIAL CHAIN DEMO")
        print(f"{Fore.GREEN}{'='*60}")
        print(f"{Fore.WHITE}This chain analyzes deck composition → generates strategy guide\n")
        
        deck_name = self.select_deck()
        deck_summary = self.deck_loader.get_deck_summary(deck_name)
        
        print(f"\n{Fore.YELLOW}Running simple sequential chain...")
        print(f"{Fore.WHITE}Chain flow: Deck Analysis → Strategy Guide\n")
        
        # Toggle verbosity
        self.deck_builder.simple_chain.verbose = self.verbose
        
        result = self.deck_builder.analyze_deck_simple(deck_summary)
        
        print(f"\n{Fore.GREEN}Final Strategy Guide:")
        print(f"{Fore.WHITE}{result}")
    
    def demo_complex_sequential(self):
        """Demo 2: Complex Sequential Chain"""
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}COMPLEX SEQUENTIAL CHAIN DEMO")
        print(f"{Fore.GREEN}{'='*60}")
        print(f"{Fore.WHITE}This chain performs: Weakness Analysis → Meta Analysis → Improvements → Optimization\n")
        
        deck_name = self.select_deck()
        deck_summary = self.deck_loader.get_deck_summary(deck_name)
        card_texts = "\n".join(self.deck_loader.get_card_texts(deck_name)[:10])
        
        print(f"\n{Fore.YELLOW}Running complex sequential chain (4 steps)...")
        
        # Toggle verbosity
        self.deck_builder.complex_chain.verbose = self.verbose
        
        result = self.deck_builder.optimize_deck_complex(deck_summary, card_texts)
        
        print(f"\n{Fore.GREEN}Chain Results:")
        for key, value in result.items():
            if key not in ['deck_summary', 'card_texts']:
                print(f"\n{Fore.CYAN}{key.replace('_', ' ').title()}:")
                print(f"{Fore.WHITE}{value[:500]}...")  # Show first 500 chars
    
    def demo_strategy_analysis(self):
        """Demo 3: Strategy Analysis Chain"""
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}STRATEGY ANALYSIS CHAIN DEMO")
        print(f"{Fore.GREEN}{'='*60}")
        print(f"{Fore.WHITE}This chain: Identifies Combos → Creates Game Plan → Analyzes Counters → Matchup Guide\n")
        
        deck_name = self.select_deck()
        deck_summary = self.deck_loader.get_deck_summary(deck_name)
        card_texts = "\n".join(self.deck_loader.get_card_texts(deck_name)[:10])
        
        print(f"\n{Fore.YELLOW}Running strategy analysis chain...")
        
        # Toggle verbosity
        self.strategy_analyzer.strategy_chain.verbose = self.verbose
        
        result = self.strategy_analyzer.analyze_strategy(deck_summary, card_texts)
        
        print(f"\n{Fore.GREEN}Strategy Analysis Results:")
        for key, value in result.items():
            if key not in ['deck_summary', 'card_texts']:
                print(f"\n{Fore.CYAN}{key.replace('_', ' ').title()}:")
                print(f"{Fore.WHITE}{value[:500]}...")
    
    def demo_router_chain(self):
        """Demo 4: Router Chain"""
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}ROUTER CHAIN DEMO")
        print(f"{Fore.GREEN}{'='*60}")
        print(f"{Fore.WHITE}Ask any Primal TCG question - it will be routed to the appropriate expert!\n")
        
        print(self.router.get_expert_list())
        
        while True:
            question = input(f"\n{Fore.CYAN}Enter your question (or 'back' to return): ").strip()
            
            if question.lower() == 'back':
                break
            
            if not question:
                print(f"{Fore.RED}Please enter a question.")
                continue
            
            print(f"\n{Fore.YELLOW}Routing question to appropriate expert...")
            
            # Toggle verbosity
            self.router.router_chain.verbose = self.verbose
            
            response = self.router.route_question(question)
            print(f"\n{Fore.GREEN}Expert Response:")
            print(f"{Fore.WHITE}{response}")
    
    def demo_competitive_analysis(self):
        """Demo 5: Competitive Analysis"""
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}COMPETITIVE ANALYSIS CHAIN DEMO")
        print(f"{Fore.GREEN}{'='*60}")
        print(f"{Fore.WHITE}Full tournament-level analysis with 5 analytical stages\n")
        
        deck_name = self.select_deck()
        deck_summary = self.deck_loader.get_deck_summary(deck_name)
        card_texts = "\n".join(self.deck_loader.get_card_texts(deck_name)[:10])
        
        print(f"\n{Fore.YELLOW}Choose analysis type:")
        print("1. Full Competitive Analysis (5-chain process)")
        print("2. Quick Tier Assessment")
        
        choice = input(f"{Fore.CYAN}Choice (1-2): ").strip()
        
        if choice == "1":
            print(f"\n{Fore.YELLOW}Running full competitive analysis...")
            print(f"{Fore.WHITE}This will analyze: Power Level → Matchups → Tech Cards → Tournament Prep → Summary\n")
            
            # Toggle verbosity
            self.competitive_analyzer.competitive_chain.verbose = self.verbose
            
            result = self.competitive_analyzer.analyze_deck_competitive(deck_summary, card_texts)
            
            print(f"\n{Fore.GREEN}Competitive Analysis Results:")
            
            # Show executive summary first
            if 'executive_summary' in result:
                print(f"\n{Fore.CYAN}Executive Summary:")
                print(f"{Fore.WHITE}{result['executive_summary']}")
            
            # Show other results
            for key, value in result.items():
                if key not in ['deck_summary', 'card_texts', 'executive_summary', 'meta_context']:
                    print(f"\n{Fore.CYAN}{key.replace('_', ' ').title()}:")
                    print(f"{Fore.WHITE}{value[:500]}...")
        
        elif choice == "2":
            print(f"\n{Fore.YELLOW}Running quick tier assessment...")
            result = self.competitive_analyzer.quick_tier_assessment(deck_summary)
            print(f"\n{Fore.GREEN}Quick Assessment:")
            print(f"{Fore.WHITE}{result}")
    
    def demo_compare_decks(self):
        """Demo 6: Compare Two Decks"""
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}DECK COMPARISON DEMO")
        print(f"{Fore.GREEN}{'='*60}\n")
        
        print(f"{Fore.YELLOW}Select first deck:")
        deck1_name = self.select_deck()
        deck1_summary = self.deck_loader.get_deck_summary(deck1_name)
        
        print(f"\n{Fore.YELLOW}Select second deck:")
        deck2_name = self.select_deck()
        deck2_summary = self.deck_loader.get_deck_summary(deck2_name)
        
        print(f"\n{Fore.YELLOW}Choose comparison type:")
        print("1. Strategic Comparison (deck building)")
        print("2. Head-to-Head Matchup Analysis")
        print("3. Merge/Hybrid Deck Creation")
        
        choice = input(f"{Fore.CYAN}Choice (1-3): ").strip()
        
        if choice == "1":
            print(f"\n{Fore.YELLOW}Comparing deck strategies...")
            comparison = self.deck_loader.compare_decks(deck1_name, deck2_name)
            
            print(f"\n{Fore.GREEN}Deck Comparison:")
            for key, value in comparison.items():
                print(f"{Fore.CYAN}{key}: {Fore.WHITE}{value}")
        
        elif choice == "2":
            print(f"\n{Fore.YELLOW}Analyzing head-to-head matchup...")
            result = self.competitive_analyzer.head_to_head_analysis(deck1_summary, deck2_summary)
            print(f"\n{Fore.GREEN}Matchup Analysis:")
            print(f"{Fore.WHITE}{result}")
        
        elif choice == "3":
            print(f"\n{Fore.YELLOW}Creating hybrid deck design...")
            
            # Toggle verbosity
            self.deck_builder.verbose = self.verbose
            
            result = self.deck_builder.compare_and_merge_decks(deck1_summary, deck2_summary)
            print(f"\n{Fore.GREEN}Hybrid Deck Design:")
            print(f"{Fore.WHITE}{result}")
    
    def demo_deck_statistics(self):
        """Demo 7: Show Deck Statistics"""
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}DECK STATISTICS")
        print(f"{Fore.GREEN}{'='*60}\n")
        
        deck_name = self.select_deck()
        
        print(f"\n{Fore.YELLOW}Analyzing {deck_name}...")
        
        # Get deck analysis
        analysis = self.deck_loader.analyze_deck_composition(deck_name)
        
        print(f"\n{Fore.GREEN}Deck Composition Analysis:")
        print(f"{Fore.CYAN}Total Cards: {Fore.WHITE}{analysis['total_cards']}")
        
        print(f"\n{Fore.CYAN}Card Types:")
        for card_type, count in analysis['card_types'].items():
            print(f"  {Fore.WHITE}{card_type}: {count}")
        
        print(f"\n{Fore.CYAN}Skills/Archetypes:")
        for skill, count in analysis['skills'].items():
            print(f"  {Fore.WHITE}{skill}: {count}")
        
        print(f"\n{Fore.CYAN}Mana Curve:")
        for cost, count in sorted(analysis['mana_curve'].items()):
            bar = "█" * count
            print(f"  {Fore.WHITE}Turn {cost}: {bar} ({count})")
        
        print(f"\n{Fore.CYAN}Elements:")
        for element, count in analysis['elements'].items():
            print(f"  {Fore.WHITE}{element}: {count}")
        
        print(f"\n{Fore.CYAN}Ability Cost Types: {Fore.WHITE}{', '.join(analysis['ability_cost_types'])}")
    
    def toggle_verbosity(self):
        """Toggle verbose output for chains"""
        self.verbose = not self.verbose
        self.deck_builder.verbose = self.verbose
        self.strategy_analyzer.verbose = self.verbose
        self.router.verbose = self.verbose
        self.competitive_analyzer.verbose = self.verbose
        
        print(f"\n{Fore.YELLOW}Verbosity {'enabled' if self.verbose else 'disabled'}")
        print(f"{Fore.WHITE}Chain execution will {'show' if self.verbose else 'hide'} intermediate steps")
    
    def run(self):
        """Main demo loop"""
        while True:
            self.display_menu()
            
            choice = input(f"\n{Fore.CYAN}Enter your choice (0-8): ").strip()
            
            if choice == "0":
                print(f"\n{Fore.YELLOW}Thank you for using Primal TCG Chain Analysis System!")
                print(f"{Fore.GREEN}May your combos always resolve! 🎮")
                break
            elif choice == "1":
                self.demo_simple_sequential()
            elif choice == "2":
                self.demo_complex_sequential()
            elif choice == "3":
                self.demo_strategy_analysis()
            elif choice == "4":
                self.demo_router_chain()
            elif choice == "5":
                self.demo_competitive_analysis()
            elif choice == "6":
                self.demo_compare_decks()
            elif choice == "7":
                self.demo_deck_statistics()
            elif choice == "8":
                self.toggle_verbosity()
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.")
            
            if choice in ["1", "2", "3", "5", "6", "7"]:
                input(f"\n{Fore.YELLOW}Press Enter to continue...")


if __name__ == "__main__":
    try:
        demo = InteractiveDemo()
        demo.run()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Demo interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}Error: {e}")
        sys.exit(1)