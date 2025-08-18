"""
Deck Builder Chain - Sequential chains for deck optimization in Primal TCG
Demonstrates both SimpleSequentialChain and SequentialChain
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()


class DeckWeakness(BaseModel):
    """Structure for deck weakness analysis"""
    weakness_type: str = Field(description="Type of weakness (e.g., 'Mana Curve', 'Synergy', 'Defense')")
    description: str = Field(description="Description of the weakness")
    severity: str = Field(description="Severity level: Low, Medium, High")
    affected_cards: List[str] = Field(description="Cards affected by this weakness")


class DeckImprovement(BaseModel):
    """Structure for deck improvement suggestions"""
    cards_to_remove: List[str] = Field(description="Cards to remove from deck")
    cards_to_add: List[str] = Field(description="Cards to add to deck")
    reasoning: str = Field(description="Reasoning for the changes")
    expected_improvement: str = Field(description="Expected improvement to deck performance")


class DeckBuilderChain:
    def __init__(self, temperature: float = 0.7):
        self.llm = ChatOpenAI(temperature=temperature, model="gpt-3.5-turbo")
        self.verbose = True
        
        # Initialize all chains
        self.simple_chain = self._create_simple_sequential_chain()
        self.complex_chain = self._create_complex_sequential_chain()
    
    def _create_simple_sequential_chain(self) -> SimpleSequentialChain:
        """
        Create a simple sequential chain for basic deck analysis
        Chain 1: Analyze deck composition -> Chain 2: Generate strategy summary
        """
        
        # Chain 1: Analyze deck composition
        composition_prompt = ChatPromptTemplate.from_template(
            """You are a Primal TCG deck expert. Analyze this deck composition and identify the main strategy:

Deck Data:
{deck_summary}

Provide a clear analysis of:
1. Main archetype (Aggro/Control/Combo/Midrange)
2. Key skill synergies (PIRATE, SIN, MICROMON, etc.)
3. Mana curve evaluation
4. Win conditions

Analysis:"""
        )
        composition_chain = LLMChain(llm=self.llm, prompt=composition_prompt)
        
        # Chain 2: Generate strategy guide based on composition
        strategy_prompt = ChatPromptTemplate.from_template(
            """Based on this deck analysis, create a concise strategy guide for playing this deck:

{deck_analysis}

Provide:
1. Opening hand priorities (what to mulligan for)
2. Early game plan (turns 1-3)
3. Mid game transitions (turns 4-6)
4. Late game win conditions
5. Key combos to execute

Strategy Guide:"""
        )
        strategy_chain = LLMChain(llm=self.llm, prompt=strategy_prompt)
        
        # Combine into simple sequential chain
        simple_chain = SimpleSequentialChain(
            chains=[composition_chain, strategy_chain],
            verbose=self.verbose
        )
        
        return simple_chain
    
    def _create_complex_sequential_chain(self) -> SequentialChain:
        """
        Create a complex sequential chain with multiple inputs/outputs
        for comprehensive deck building
        """
        
        # Chain 1: Analyze current deck weaknesses
        weakness_prompt = ChatPromptTemplate.from_template(
            """As a Primal TCG expert, analyze this deck for weaknesses:

Deck Composition:
{deck_summary}

Card Texts Sample:
{card_texts}

Identify and describe:
1. Mana curve issues
2. Lack of key effects (removal, draw, etc.)
3. Vulnerability to specific strategies
4. Missing synergies
5. Consistency problems

Detailed Weakness Analysis:"""
        )
        weakness_chain = LLMChain(
            llm=self.llm, 
            prompt=weakness_prompt,
            output_key="weakness_analysis"
        )
        
        # Chain 2: Analyze meta matchups
        meta_prompt = ChatPromptTemplate.from_template(
            """Given this deck's weaknesses, analyze how it performs against meta decks:

Weaknesses:
{weakness_analysis}

Original Deck:
{deck_summary}

Analyze matchups against:
1. Aggro PIRATE decks
2. Control SIN decks  
3. Combo MICROMON decks
4. Midrange MECHA decks

Provide win rates and key cards for each matchup.

Meta Analysis:"""
        )
        meta_chain = LLMChain(
            llm=self.llm,
            prompt=meta_prompt,
            output_key="meta_analysis"
        )
        
        # Chain 3: Suggest improvements based on weaknesses and meta
        improvement_prompt = ChatPromptTemplate.from_template(
            """Based on the deck's weaknesses and meta position, suggest specific improvements:

Weakness Analysis:
{weakness_analysis}

Meta Analysis:
{meta_analysis}

Original Deck Summary:
{deck_summary}

Suggest:
1. Specific cards to remove (and why)
2. Specific cards to add (and why)
3. Changes to mana base/curve
4. Sideboard recommendations
5. Alternative build paths

Format as actionable changes with clear reasoning.

Improvement Plan:"""
        )
        improvement_chain = LLMChain(
            llm=self.llm,
            prompt=improvement_prompt,
            output_key="improvement_plan"
        )
        
        # Chain 4: Generate final optimized deck list
        optimization_prompt = ChatPromptTemplate.from_template(
            """Create the final optimized deck list based on all analysis:

Original Deck:
{deck_summary}

Improvements:
{improvement_plan}

Generate:
1. Core cards (must-have)
2. Flex slots (adjustable based on meta)
3. Ideal mana curve distribution
4. Skill/archetype focus
5. Win condition priority

Optimized Deck Configuration:"""
        )
        optimization_chain = LLMChain(
            llm=self.llm,
            prompt=optimization_prompt,
            output_key="optimized_deck"
        )
        
        # Combine into complex sequential chain
        complex_chain = SequentialChain(
            chains=[weakness_chain, meta_chain, improvement_chain, optimization_chain],
            input_variables=["deck_summary", "card_texts"],
            output_variables=["weakness_analysis", "meta_analysis", 
                            "improvement_plan", "optimized_deck"],
            verbose=self.verbose
        )
        
        return complex_chain
    
    def analyze_deck_simple(self, deck_summary: str) -> str:
        """Run simple sequential chain for basic deck analysis"""
        return self.simple_chain.run(deck_summary)
    
    def optimize_deck_complex(self, deck_summary: str, card_texts: str) -> Dict:
        """Run complex sequential chain for comprehensive deck optimization"""
        result = self.complex_chain({
            "deck_summary": deck_summary,
            "card_texts": card_texts[:3000]  # Limit text length
        })
        return result
    
    def compare_and_merge_decks(self, deck1_summary: str, deck2_summary: str) -> str:
        """
        Special chain to compare two decks and suggest a merged/hybrid build
        """
        
        # Combine deck summaries into single input for SimpleSequentialChain
        combined_decks = f"""Deck 1:
{deck1_summary}

Deck 2:
{deck2_summary}"""
        
        # Chain 1: Compare deck strategies (single input)
        compare_prompt = ChatPromptTemplate.from_template(
            """Compare these two Primal TCG decks and identify complementary strategies:

{input}

Identify:
1. Shared strategies/skills
2. Complementary strengths
3. Conflicting elements
4. Potential synergies if merged

Comparison:"""
        )
        compare_chain = LLMChain(llm=self.llm, prompt=compare_prompt)
        
        # Chain 2: Create hybrid deck
        hybrid_prompt = ChatPromptTemplate.from_template(
            """Based on this deck comparison, create an optimal hybrid deck:

{input}

Design a new deck that:
1. Combines the best elements of both
2. Maintains consistency
3. Has clear win conditions
4. Balances the mana curve

Hybrid Deck Design:"""
        )
        hybrid_chain = LLMChain(llm=self.llm, prompt=hybrid_prompt)
        
        # Create and run the chain
        merge_chain = SimpleSequentialChain(
            chains=[compare_chain, hybrid_chain],
            verbose=self.verbose
        )
        
        return merge_chain.run(combined_decks)