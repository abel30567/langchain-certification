"""
Competitive Analysis Chain - Comprehensive competitive deck analysis
Combines multiple chain types for tournament-level analysis
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain, SequentialChain
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

load_dotenv()


class CompetitiveAnalysisChain:
    def __init__(self, temperature: float = 0.7):
        self.llm = ChatOpenAI(temperature=temperature, model="gpt-3.5-turbo")
        self.analytical_llm = ChatOpenAI(temperature=0.3, model="gpt-3.5-turbo")  # Lower temp for analysis
        self.verbose = True
        
        # Initialize comprehensive competitive chain
        self.competitive_chain = self._create_competitive_chain()
    
    def _create_competitive_chain(self) -> SequentialChain:
        """
        Create a comprehensive competitive analysis chain
        This is our most complex chain combining multiple analytical steps
        """
        
        # Chain 1: Deck Power Level Assessment
        power_level_prompt = ChatPromptTemplate.from_template(
            """Assess the competitive power level of this Primal TCG deck:

Deck Summary:
{deck_summary}

Card Texts (for ability analysis):
{card_texts}

Meta Context:
{meta_context}

Evaluate:
1. Raw Power Level (1-10 scale)
   - Card quality
   - Synergy strength
   - Win condition reliability

2. Speed Rating (1-10 scale)
   - Average turn to win
   - Setup requirements
   - Interaction capability

3. Consistency Rating (1-10 scale)
   - Mulligan reliability
   - Draw dependency
   - Backup plans

4. Resilience Rating (1-10 scale)
   - Recovery from disruption
   - Removal resistance
   - Resource management

5. Overall Tier Placement (S/A/B/C/D)

Provide specific examples and card references.

Power Level Assessment:"""
        )
        power_level_chain = LLMChain(
            llm=self.analytical_llm,
            prompt=power_level_prompt,
            output_key="power_assessment"
        )
        
        # Chain 2: Matchup Spread Analysis
        matchup_spread_prompt = ChatPromptTemplate.from_template(
            """Analyze this deck's matchup spread against the competitive field:

Deck Power Assessment:
{power_assessment}

Deck Summary:
{deck_summary}

Current Meta:
{meta_context}

Provide detailed matchup analysis:
1. Favorable Matchups (60%+ win rate)
   - Why you're favored
   - Key cards in matchup
   - Game plan adjustments

2. Even Matchups (45-55% win rate)
   - Deciding factors
   - Play/draw dependency
   - Skill-testing decisions

3. Unfavorable Matchups (< 45% win rate)
   - Main problems
   - Potential tech cards
   - Sideboard solutions

4. Overall Meta Position
   - Expected win rate
   - Tournament viability
   - Recommendation level

Include specific percentages and reasoning.

Matchup Spread Analysis:"""
        )
        matchup_spread_chain = LLMChain(
            llm=self.llm,
            prompt=matchup_spread_prompt,
            output_key="matchup_analysis"
        )
        
        # Chain 3: Tech Card and Adaptation Recommendations
        tech_prompt = ChatPromptTemplate.from_template(
            """Based on the matchup analysis, recommend tech cards and adaptations:

Matchup Analysis:
{matchup_analysis}

Power Assessment:
{power_assessment}

Original Deck:
{deck_summary}

Recommend:
1. Main Deck Tech Options
   - Cards to add (with what to cut)
   - Ratio adjustments
   - Meta calls

2. Sideboard Construction (15 cards)
   - Core sideboard cards (must-haves)
   - Flex slots based on meta
   - Specific sideboard plans per matchup

3. Alternative Builds
   - More aggressive version
   - More controlling version
   - Anti-meta version

4. Card Upgrades
   - Budget options vs optimal choices
   - Future set considerations
   - Power creep adjustments

Provide specific card names and quantities.

Tech and Adaptation Guide:"""
        )
        tech_chain = LLMChain(
            llm=self.llm,
            prompt=tech_prompt,
            output_key="tech_guide"
        )
        
        # Chain 4: Tournament Preparation Guide
        tournament_prep_prompt = ChatPromptTemplate.from_template(
            """Create a comprehensive tournament preparation guide:

Power Assessment:
{power_assessment}

Matchup Analysis:
{matchup_analysis}

Tech Guide:
{tech_guide}

Create:
1. Practice Plan (1 week before tournament)
   - Day-by-day schedule
   - Specific matchups to practice
   - Skills to develop

2. Mental Notes Sheet
   - Key decision points
   - Common mistakes to avoid
   - Timing windows to remember

3. Sideboard Guide (quick reference)
   - IN/OUT for each matchup
   - When to pivot strategies
   - Counter-sideboarding

4. Tournament Day Checklist
   - Deck registration tips
   - Energy management
   - Adaptation between rounds

5. Expected Meta Breakdown
   - % of each archetype
   - Rounds to expect them
   - Positioning strategy

Tournament Preparation Guide:"""
        )
        tournament_prep_chain = LLMChain(
            llm=self.llm,
            prompt=tournament_prep_prompt,
            output_key="tournament_guide"
        )
        
        # Chain 5: Executive Summary and Action Items
        summary_prompt = ChatPromptTemplate.from_template(
            """Create an executive summary with clear action items:

Power Assessment:
{power_assessment}

Matchup Analysis:
{matchup_analysis}

Tech Guide:
{tech_guide}

Tournament Guide:
{tournament_guide}

Provide:
1. Executive Summary (3-5 sentences)
   - Deck viability verdict
   - Best use cases
   - Key strengths/weaknesses

2. Immediate Action Items (prioritized)
   - Essential changes before playing
   - Testing priorities
   - Cards to acquire

3. Success Metrics
   - What constitutes success with this deck
   - Realistic tournament expectations
   - Improvement benchmarks

4. Final Recommendation
   - Play it or shelf it?
   - Investment worth it?
   - Skill requirement assessment

Competitive Analysis Summary:"""
        )
        summary_chain = LLMChain(
            llm=self.analytical_llm,
            prompt=summary_prompt,
            output_key="executive_summary"
        )
        
        # Combine all chains
        competitive_chain = SequentialChain(
            chains=[
                power_level_chain,
                matchup_spread_chain,
                tech_chain,
                tournament_prep_chain,
                summary_chain
            ],
            input_variables=["deck_summary", "card_texts", "meta_context"],
            output_variables=[
                "power_assessment",
                "matchup_analysis",
                "tech_guide",
                "tournament_guide",
                "executive_summary"
            ],
            verbose=self.verbose
        )
        
        return competitive_chain
    
    def analyze_deck_competitive(self, 
                                deck_summary: str, 
                                card_texts: str,
                                meta_context: str = "Diverse meta with PIRATE aggro (25%), SIN control (20%), MICROMON combo (15%), MECHA midrange (20%), Other (20%)") -> Dict:
        """Run the full competitive analysis"""
        return self.competitive_chain({
            "deck_summary": deck_summary,
            "card_texts": card_texts[:3000],  # Limit for tokens
            "meta_context": meta_context
        })
    
    def quick_tier_assessment(self, deck_summary: str) -> str:
        """Quick tier assessment without full analysis"""
        
        quick_prompt = ChatPromptTemplate.from_template(
            """Quickly assess this Primal TCG deck's competitive tier:

Deck:
{deck_summary}

Provide:
1. Tier (S/A/B/C/D)
2. One-line reasoning
3. Biggest strength
4. Biggest weakness
5. Similar successful decks

Quick Assessment:"""
        )
        
        quick_chain = LLMChain(llm=self.analytical_llm, prompt=quick_prompt)
        return quick_chain.run(deck_summary=deck_summary)
    
    def head_to_head_analysis(self, deck1_summary: str, deck2_summary: str) -> str:
        """Analyze head-to-head matchup between two specific decks"""
        
        h2h_prompt = ChatPromptTemplate.from_template(
            """Analyze the head-to-head matchup between these two Primal TCG decks:

Deck 1:
{deck1}

Deck 2:
{deck2}

Provide:
1. Win rate prediction (Deck 1 vs Deck 2)
2. Key cards in the matchup for each side
3. Game flow analysis
   - Who's the beatdown?
   - Critical turns
   - Decision points

4. Sideboarding for both sides
5. Play/draw importance
6. Skill ceiling in the matchup

Head-to-Head Analysis:"""
        )
        
        h2h_chain = LLMChain(llm=self.llm, prompt=h2h_prompt)
        return h2h_chain.run(deck1=deck1_summary, deck2=deck2_summary)