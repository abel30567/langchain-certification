#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick test to verify all imports work correctly
"""

try:
    print("Testing imports...")
    
    # Test utility imports
    from utils.data_loader import DeckLoader
    print("✓ Data loader imported")
    
    # Test chain imports
    from chains.deck_builder_chain import DeckBuilderChain
    print("✓ Deck builder chain imported")
    
    from chains.strategy_chain import StrategyAnalysisChain
    print("✓ Strategy chain imported")
    
    from chains.router_chain import PrimalTCGRouterChain
    print("✓ Router chain imported")
    
    from chains.competitive_chain import CompetitiveAnalysisChain
    print("✓ Competitive chain imported")
    
    # Test data loading
    loader = DeckLoader()
    decks = loader.get_all_deck_names()
    print(f"✓ Loaded {len(decks)} decks: {decks}")
    
    # Test basic deck analysis
    if decks:
        analysis = loader.analyze_deck_composition(decks[0])
        print(f"✓ Analyzed {decks[0]}: {analysis['total_cards']} cards")
    
    print("\n✅ All imports and basic functions working!")
    print("You can now run:")
    print("  python demo_interactive.py")
    print("  python demo_automatic.py")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nMake sure you have:")
    print("1. Installed requirements: pip install -r requirements.txt")
    print("2. Set OPENAI_API_KEY in .env file")
    import traceback
    traceback.print_exc()

if __name__ == "__main__":
    pass