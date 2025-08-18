"""
Automatic Demo for Primal TCG Chains
Demonstrates all chain types automatically without user input
"""

import os
import time
from colorama import init, Fore, Style
from utils.data_loader import DeckLoader
from chains.deck_builder_chain import DeckBuilderChain
from chains.strategy_chain import StrategyAnalysisChain
from chains.router_chain import PrimalTCGRouterChain
from chains.competitive_chain import CompetitiveAnalysisChain

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


class AutomaticDemo:
    def __init__(self):
        print_section("🎮 PRIMAL TCG CHAINS - AUTOMATIC DEMONSTRATION 🎮", Fore.MAGENTA)
        print(f"{Fore.WHITE}This demo will automatically showcase all chain types")
        print(f"{Fore.WHITE}implemented in Lesson 3: Chains\n")
        pause(2)
        
        # Initialize components
        print(f"{Fore.YELLOW}Initializing systems...")
        self.deck_loader = DeckLoader()
        self.deck_builder = DeckBuilderChain()
        self.strategy_analyzer = StrategyAnalysisChain()
        self.router = PrimalTCGRouterChain()
        self.competitive_analyzer = CompetitiveAnalysisChain()
        
        # Set chains to non-verbose for cleaner demo
        self.deck_builder.simple_chain.verbose = False
        self.deck_builder.complex_chain.verbose = False
        self.strategy_analyzer.strategy_chain.verbose = False
        self.router.router_chain.verbose = False
        self.competitive_analyzer.competitive_chain.verbose = False
        
        print(f"{Fore.GREEN}✓ All systems initialized\n")
        pause(1)
    
    def demo_1_simple_sequential(self):
        """Demonstrate SimpleSequentialChain"""
        print_section("DEMO 1: SimpleSequentialChain", Fore.GREEN)
        print(f"{Fore.WHITE}Concept: Chains that pass output directly from one to the next")
        print(f"{Fore.WHITE}Example: Deck Analysis → Strategy Guide\n")
        pause(2)
        
        # Use deck1 (PIRATE/MECHA deck)
        deck_name = "deck1"
        print(f"{Fore.CYAN}Selected Deck: {deck_name} (Mixed Strategy Deck)")
        
        deck_summary = self.deck_loader.get_deck_summary(deck_name)
        print(f"\n{Fore.WHITE}Deck Statistics:")
        analysis = self.deck_loader.analyze_deck_composition(deck_name)
        print(f"  • Total Cards: {analysis['total_cards']}")
        print(f"  • Main Skills: {', '.join(list(analysis['skills'].keys())[:3])}")
        pause(2)
        
        print_subsection("Running SimpleSequentialChain")
        print(f"{Fore.WHITE}Chain 1: Analyzing deck composition...")
        print(f"{Fore.WHITE}Chain 2: Generating strategy guide...")
        
        result = self.deck_builder.analyze_deck_simple(deck_summary)
        
        print(f"\n{Fore.GREEN}Result - Strategy Guide:")
        print(f"{Fore.WHITE}{result[:600]}...")
        pause(3)
    
    def demo_2_complex_sequential(self):
        """Demonstrate SequentialChain with named inputs/outputs"""
        print_section("DEMO 2: SequentialChain (Complex)", Fore.GREEN)
        print(f"{Fore.WHITE}Concept: Chains with named inputs/outputs for complex workflows")
        print(f"{Fore.WHITE}Example: 4-step deck optimization process\n")
        pause(2)
        
        # Use deck2 (SIN deck)
        deck_name = "deck2"
        print(f"{Fore.CYAN}Selected Deck: {deck_name} (SIN Control Deck)")
        
        deck_summary = self.deck_loader.get_deck_summary(deck_name)
        card_texts = "\n".join(self.deck_loader.get_card_texts(deck_name)[:5])
        
        print_subsection("Running 4-Stage SequentialChain")
        print(f"{Fore.WHITE}Stage 1: Weakness Analysis")
        print(f"{Fore.WHITE}Stage 2: Meta Matchup Analysis")
        print(f"{Fore.WHITE}Stage 3: Improvement Suggestions")
        print(f"{Fore.WHITE}Stage 4: Optimized Deck Configuration\n")
        
        result = self.deck_builder.optimize_deck_complex(deck_summary, card_texts)
        
        # Show key outputs
        for stage_num, (key, value) in enumerate(result.items(), 1):
            if key not in ['deck_summary', 'card_texts']:
                stage_names = {
                    'weakness_analysis': 'Weakness Analysis',
                    'meta_analysis': 'Meta Matchup Analysis',
                    'improvement_plan': 'Improvement Plan',
                    'optimized_deck': 'Optimized Configuration'
                }
                if key in stage_names:
                    print(f"\n{Fore.CYAN}Stage Output - {stage_names[key]}:")
                    print(f"{Fore.WHITE}{value[:400]}...")
                    pause(1)
    
    def demo_3_router_chain(self):
        """Demonstrate Router Chain (MultiPromptChain)"""
        print_section("DEMO 3: Router Chain (MultiPromptChain)", Fore.GREEN)
        print(f"{Fore.WHITE}Concept: Routes questions to specialized expert chains")
        print(f"{Fore.WHITE}7 Expert Systems: Rules, Deck Building, Strategy, Meta, Trading, Beginner, Lore\n")
        pause(2)
        
        # Sample questions for different experts
        test_questions = [
            ("How does TRIGGER stacking work?", "rules_expert"),
            ("What's the best mana curve for aggro?", "deckbuilding_expert"),
            ("How do I beat control decks?", "strategy_expert"),
            ("What decks are dominating tournaments?", "meta_expert"),
            ("Is Flame Dragon Alpha worth investing in?", "trading_expert"),
            ("I'm new, what deck should I start with?", "beginner_expert"),
            ("What's the story behind the SIN faction?", "lore_expert")
        ]
        
        print_subsection("Testing Router with Various Questions")
        
        for i, (question, expected_expert) in enumerate(test_questions[:3], 1):  # Show first 3
            print(f"{Fore.CYAN}Question {i}: {question}")
            print(f"{Fore.YELLOW}Expected Expert: {expected_expert}")
            
            response = self.router.route_question(question)
            print(f"{Fore.GREEN}Response Preview:")
            print(f"{Fore.WHITE}{response[:300]}...\n")
            pause(2)
        
        print(f"{Fore.YELLOW}(Demonstrated 3 of 7 expert systems)")
    
    def demo_4_strategy_chains(self):
        """Demonstrate Strategy Analysis Chains"""
        print_section("DEMO 4: Strategy Analysis Chains", Fore.GREEN)
        print(f"{Fore.WHITE}Concept: Deep analysis of combos, synergies, and game plans")
        print(f"{Fore.WHITE}4-stage analysis: Combos → Game Plan → Counters → Matchups\n")
        pause(2)
        
        # Use deck3 (MICROMON deck)
        deck_name = "deck3"
        print(f"{Fore.CYAN}Selected Deck: {deck_name} (MICROMON Combo Deck)")
        
        deck_summary = self.deck_loader.get_deck_summary(deck_name)
        card_texts = "\n".join(self.deck_loader.get_card_texts(deck_name)[:5])
        
        print_subsection("Running Strategy Analysis Chain")
        
        result = self.strategy_analyzer.analyze_strategy(deck_summary, card_texts)
        
        # Show each stage
        stages = ['combo_analysis', 'game_plan', 'counter_strategies', 'matchup_guide']
        stage_names = {
            'combo_analysis': 'Combo Identification',
            'game_plan': 'Turn-by-Turn Game Plan',
            'counter_strategies': 'Counter-Strategy Analysis',
            'matchup_guide': 'Matchup-Specific Guide'
        }
        
        for stage in stages[:2]:  # Show first 2 stages
            if stage in result:
                print(f"\n{Fore.CYAN}{stage_names[stage]}:")
                print(f"{Fore.WHITE}{result[stage][:400]}...")
                pause(2)
    
    def demo_5_competitive_analysis(self):
        """Demonstrate Competitive Analysis Chain"""
        print_section("DEMO 5: Competitive Analysis (Tournament-Level)", Fore.GREEN)
        print(f"{Fore.WHITE}Concept: Comprehensive 5-stage competitive deck evaluation")
        print(f"{Fore.WHITE}Most complex chain combining multiple analytical perspectives\n")
        pause(2)
        
        deck_name = "deck1"
        print(f"{Fore.CYAN}Analyzing: {deck_name} for competitive play")
        
        deck_summary = self.deck_loader.get_deck_summary(deck_name)
        
        print_subsection("Quick Tier Assessment")
        quick_result = self.competitive_analyzer.quick_tier_assessment(deck_summary)
        print(f"{Fore.WHITE}{quick_result}")
        pause(2)
        
        print_subsection("5-Stage Competitive Analysis Process")
        print(f"{Fore.WHITE}1. Power Level Assessment (1-10 scales)")
        print(f"{Fore.WHITE}2. Matchup Spread Analysis")
        print(f"{Fore.WHITE}3. Tech Card Recommendations")
        print(f"{Fore.WHITE}4. Tournament Preparation Guide")
        print(f"{Fore.WHITE}5. Executive Summary & Action Items\n")
        
        card_texts = "\n".join(self.deck_loader.get_card_texts(deck_name)[:5])
        result = self.competitive_analyzer.analyze_deck_competitive(deck_summary, card_texts)
        
        # Show executive summary
        if 'executive_summary' in result:
            print(f"{Fore.CYAN}Executive Summary:")
            print(f"{Fore.WHITE}{result['executive_summary'][:600]}...")
    
    def demo_6_deck_comparison(self):
        """Demonstrate Deck Comparison Chains"""
        print_section("DEMO 6: Deck Comparison & Hybrid Creation", Fore.GREEN)
        print(f"{Fore.WHITE}Concept: Compare decks and create optimal hybrid builds\n")
        pause(2)
        
        deck1_name = "deck1"
        deck2_name = "deck2"
        
        print(f"{Fore.CYAN}Comparing: {deck1_name} vs {deck2_name}")
        
        # Data comparison
        comparison = self.deck_loader.compare_decks(deck1_name, deck2_name)
        
        print_subsection("Statistical Comparison")
        print(f"{Fore.WHITE}Deck 1 Focus: {comparison['deck1_focus']}")
        print(f"{Fore.WHITE}Deck 2 Focus: {comparison['deck2_focus']}")
        print(f"{Fore.WHITE}Common Skills: {comparison['common_skills']}")
        print(f"{Fore.WHITE}Card Count Difference: {comparison['card_count_diff']}")
        pause(2)
        
        print_subsection("Head-to-Head Matchup Analysis")
        deck1_summary = self.deck_loader.get_deck_summary(deck1_name)
        deck2_summary = self.deck_loader.get_deck_summary(deck2_name)
        
        h2h_result = self.competitive_analyzer.head_to_head_analysis(deck1_summary, deck2_summary)
        print(f"{Fore.WHITE}{h2h_result[:500]}...")
        pause(2)
        
        print_subsection("Creating Hybrid Deck")
        print(f"{Fore.YELLOW}Merging best elements of both decks...")
        hybrid_result = self.deck_builder.compare_and_merge_decks(deck1_summary, deck2_summary)
        print(f"{Fore.WHITE}{hybrid_result[:500]}...")
    
    def demo_7_chain_comparison(self):
        """Show comparison of chain types"""
        print_section("CHAIN TYPE COMPARISON", Fore.MAGENTA)
        
        print(f"{Fore.CYAN}Chain Types Demonstrated:\n")
        
        chain_info = [
            ("SimpleSequentialChain", "Linear flow, single input/output", "Best for: Simple workflows"),
            ("SequentialChain", "Named inputs/outputs, complex flows", "Best for: Multi-stage analysis"),
            ("RouterChain", "Dynamic routing to specialists", "Best for: Varied question types"),
            ("Custom Chains", "Domain-specific combinations", "Best for: Specialized tasks")
        ]
        
        for name, desc, use_case in chain_info:
            print(f"{Fore.GREEN}• {name}")
            print(f"{Fore.WHITE}  {desc}")
            print(f"{Fore.YELLOW}  {use_case}\n")
            pause(1)
    
    def run_summary(self):
        """Final summary of the demonstration"""
        print_section("DEMONSTRATION COMPLETE", Fore.MAGENTA)
        
        print(f"{Fore.WHITE}We've demonstrated how LangChain's chain types can be applied")
        print(f"{Fore.WHITE}to create a comprehensive Primal TCG analysis system.\n")
        
        print(f"{Fore.CYAN}Key Takeaways:")
        print(f"{Fore.WHITE}1. SimpleSequentialChain: Perfect for linear analysis flows")
        print(f"{Fore.WHITE}2. SequentialChain: Enables complex multi-stage processing")
        print(f"{Fore.WHITE}3. RouterChain: Routes to specialized experts dynamically")
        print(f"{Fore.WHITE}4. Custom Chains: Can be combined for domain-specific tasks\n")
        
        print(f"{Fore.GREEN}Applications in Primal TCG:")
        print(f"{Fore.WHITE}• Deck optimization and building")
        print(f"{Fore.WHITE}• Competitive meta analysis")
        print(f"{Fore.WHITE}• Strategy and combo identification")
        print(f"{Fore.WHITE}• Player assistance at all skill levels\n")
        
        print(f"{Fore.YELLOW}This system demonstrates both simple (2-3 chains) and")
        print(f"{Fore.YELLOW}complex (5+ chains) implementations as requested.\n")
        
        print(f"{Fore.MAGENTA}{'='*70}")
        print(f"{Fore.MAGENTA}Thank you for watching the Primal TCG Chains demonstration!")
        print(f"{Fore.MAGENTA}{'='*70}")
    
    def run(self):
        """Run the complete automatic demonstration"""
        try:
            print(f"{Fore.YELLOW}Starting automatic demonstration...\n")
            pause(2)
            
            # Run each demo
            self.demo_1_simple_sequential()
            pause(2)
            
            self.demo_2_complex_sequential()
            pause(2)
            
            self.demo_3_router_chain()
            pause(2)
            
            self.demo_4_strategy_chains()
            pause(2)
            
            self.demo_5_competitive_analysis()
            pause(2)
            
            self.demo_6_deck_comparison()
            pause(2)
            
            self.demo_7_chain_comparison()
            pause(2)
            
            self.run_summary()
            
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Demo interrupted by user.")
        except Exception as e:
            print(f"\n{Fore.RED}Error during demonstration: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    # Run the automatic demo
    demo = AutomaticDemo()
    demo.run()