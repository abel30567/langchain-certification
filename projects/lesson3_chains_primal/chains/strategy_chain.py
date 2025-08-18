"""
Strategy Analysis Chain - Analyzes combos, synergies, and game plans
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain, SequentialChain
from typing import Dict, List
import os
from dotenv import load_dotenv

load_dotenv()


class StrategyAnalysisChain:
    def __init__(self, temperature: float = 0.7):
        self.llm = ChatOpenAI(temperature=temperature, model="gpt-3.5-turbo")
        self.verbose = True
        
        # Initialize strategy analysis chain
        self.strategy_chain = self._create_strategy_chain()
        self.combo_chain = self._create_combo_analysis_chain()
    
    def _create_strategy_chain(self) -> SequentialChain:
        """
        Create a chain for comprehensive strategy analysis
        """
        
        # Chain 1: Identify key combos and synergies
        combo_identification_prompt = ChatPromptTemplate.from_template(
            """As a Primal TCG expert, identify all key combos and synergies in this deck:

Deck Summary:
{deck_summary}

Sample Card Texts (look for TRIGGER abilities and synergies):
{card_texts}

Identify:
1. Two-card combos (cards that work well together)
2. Three+ card combos (powerful multi-card interactions)
3. Skill synergies (e.g., PIRATE with PIRATE bonuses)
4. Trigger chains (TRIGGER abilities that enable other triggers)
5. Resource synergies (cards that generate/use similar resources)

Format each combo with:
- Cards involved
- How the combo works
- When to execute it
- Power level (1-10)

Combo Analysis:"""
        )
        combo_chain = LLMChain(
            llm=self.llm,
            prompt=combo_identification_prompt,
            output_key="combo_analysis"
        )
        
        # Chain 2: Develop turn-by-turn game plan
        gameplan_prompt = ChatPromptTemplate.from_template(
            """Based on the deck's combos and composition, create a detailed turn-by-turn game plan:

Deck Summary:
{deck_summary}

Key Combos:
{combo_analysis}

Create a game plan for:
1. Turns 1-2 (Early game setup)
   - Priority plays
   - Resource management
   - What to search for

2. Turns 3-4 (Development phase)
   - Board development
   - Combo setup
   - Defensive preparations

3. Turns 5-6 (Mid game)
   - Combo execution
   - Pressure application
   - Resource advantage

4. Turns 7+ (Late game)
   - Win condition execution
   - Backup plans
   - Resource recycling

Include specific card names and sequences.

Detailed Game Plan:"""
        )
        gameplan_chain = LLMChain(
            llm=self.llm,
            prompt=gameplan_prompt,
            output_key="game_plan"
        )
        
        # Chain 3: Counter-strategy analysis
        counter_prompt = ChatPromptTemplate.from_template(
            """Analyze how opponents might counter this deck's strategy and how to adapt:

Game Plan:
{game_plan}

Combos:
{combo_analysis}

Analyze:
1. Common counters to your combos
2. Disruption points in your game plan
3. Adaptation strategies when combos are disrupted
4. Backup win conditions
5. How to play around common removal/counters

Counter-Strategy Guide:"""
        )
        counter_chain = LLMChain(
            llm=self.llm,
            prompt=counter_prompt,
            output_key="counter_strategies"
        )
        
        # Chain 4: Matchup-specific adjustments
        matchup_prompt = ChatPromptTemplate.from_template(
            """Create specific strategy adjustments for different matchups:

Base Game Plan:
{game_plan}

Counter Strategies:
{counter_strategies}

Provide adjusted strategies for:
1. vs Aggro (PIRATE/Rush decks)
   - Mulligan changes
   - Defensive priorities
   - Speed adjustments

2. vs Control (SIN/Removal heavy)
   - Resource management
   - Threat deployment
   - Combo protection

3. vs Combo (MICROMON/OTK decks)
   - Race vs disrupt decisions
   - Pressure timing
   - Interaction points

4. vs Midrange (MECHA/Value decks)
   - Resource trading
   - Board control
   - Timing windows

Matchup Guide:"""
        )
        matchup_chain = LLMChain(
            llm=self.llm,
            prompt=matchup_prompt,
            output_key="matchup_guide"
        )
        
        # Combine into comprehensive strategy chain
        strategy_chain = SequentialChain(
            chains=[combo_chain, gameplan_chain, counter_chain, matchup_chain],
            input_variables=["deck_summary", "card_texts"],
            output_variables=["combo_analysis", "game_plan", 
                            "counter_strategies", "matchup_guide"],
            verbose=self.verbose
        )
        
        return strategy_chain
    
    def _create_combo_analysis_chain(self) -> LLMChain:
        """
        Specialized chain for deep combo analysis
        """
        
        combo_deep_prompt = ChatPromptTemplate.from_template(
            """Perform deep analysis of specific card combinations in Primal TCG:

Cards to analyze:
{cards_to_analyze}

For each combination:
1. Explain the interaction step-by-step
2. Calculate resource requirements (turn count, ability costs)
3. Identify setup requirements
4. Rate consistency (how often you can pull it off)
5. Calculate damage/value output
6. List cards that enhance the combo
7. List cards that counter the combo

Consider:
- TRIGGER timing and stacking
- Resource generation (cards under/attached)
- Skill synergies
- Element requirements

Deep Combo Analysis:"""
        )
        
        return LLMChain(
            llm=self.llm,
            prompt=combo_deep_prompt
        )
    
    def analyze_strategy(self, deck_summary: str, card_texts: str) -> Dict:
        """Run the comprehensive strategy analysis chain"""
        return self.strategy_chain({
            "deck_summary": deck_summary,
            "card_texts": card_texts[:3000]  # Limit for token management
        })
    
    def analyze_specific_combo(self, cards: List[str]) -> str:
        """Analyze a specific combo in detail"""
        cards_str = "\n".join([f"- {card}" for card in cards])
        return self.combo_chain.run(cards_to_analyze=cards_str)
    
    def generate_sideboard_guide(self, deck_summary: str, matchup_guide: str) -> str:
        """Generate sideboarding recommendations based on matchups"""
        
        sideboard_prompt = ChatPromptTemplate.from_template(
            """Create a comprehensive sideboard guide for this Primal TCG deck:

Deck:
{deck_summary}

Matchup Analysis:
{matchup_guide}

Recommend:
1. 15 sideboard cards with specific purposes
2. Sideboarding plans for each matchup:
   - Cards to remove
   - Cards to bring in
   - Strategy adjustments

3. Flexible slots that can be adjusted based on local meta

Format as:
[Card Name] x[Quantity] - Purpose and matchups

Sideboard Guide:"""
        )
        
        sideboard_chain = LLMChain(llm=self.llm, prompt=sideboard_prompt)
        
        return sideboard_chain.run(
            deck_summary=deck_summary,
            matchup_guide=matchup_guide
        )