#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script for the Primal TCG Rules Assistant
Demonstrates all functionality without requiring API calls
"""

import json
from datetime import datetime

def test_without_api():
    """Test the system structure without making API calls."""
    
    print("=== PRIMAL TCG RULES ASSISTANT TEST ===\n")
    print("This test demonstrates the system structure without API calls.\n")
    
    # Simulate structured parsed output
    example_parsed_questions = [
        {
            "question_type": "keyword_ability",
            "keywords_involved": ["Rush"],
            "complexity_level": 2,
            "game_phase": "main_phase",
            "cards_mentioned": [],
            "relevant_rule_sections": ["7.1.9"],
            "clarification": "Rush allows a character to attack on the turn it was summoned.",
            "follow_up_needed": False,
            "timestamp": datetime.now().isoformat(),
            "original_question": "Can I use Rush ability if my character was summoned this turn?"
        },
        {
            "question_type": "card_interaction",
            "keywords_involved": ["Transformation", "Counter"],
            "complexity_level": 4,
            "game_phase": "any_phase",
            "cards_mentioned": [],
            "relevant_rule_sections": ["7.1.1", "7.1.4", "1.2"],
            "clarification": "Counter negates the transformation effect. Can't beats can rule applies.",
            "follow_up_needed": True,
            "timestamp": datetime.now().isoformat(),
            "original_question": "If I have a character with Transformation and my opponent uses Counter on it, what happens?"
        },
        {
            "question_type": "keyword_ability",
            "keywords_involved": ["Unique"],
            "complexity_level": 3,
            "game_phase": "main_phase",
            "cards_mentioned": [],
            "relevant_rule_sections": ["7.1.3"],
            "clarification": "Only one Unique character with the same name can be in play at a time.",
            "follow_up_needed": False,
            "timestamp": datetime.now().isoformat(),
            "original_question": "What happens when two Unique characters with the same name are in play?"
        },
        {
            "question_type": "keyword_ability",
            "keywords_involved": ["Camouflage"],
            "complexity_level": 2,
            "game_phase": "any_phase",
            "cards_mentioned": [],
            "relevant_rule_sections": ["7.1.2"],
            "clarification": "Camouflage can be activated during either player's turn if you have priority.",
            "follow_up_needed": False,
            "timestamp": datetime.now().isoformat(),
            "original_question": "Can I activate Camouflage during my opponent's turn?"
        },
        {
            "question_type": "keyword_ability",
            "keywords_involved": ["Promote"],
            "complexity_level": 3,
            "game_phase": "main_phase",
            "cards_mentioned": [],
            "relevant_rule_sections": ["7.1.8", "6.2.4"],
            "clarification": "Promote can be used on damaged characters. The damage remains after promotion.",
            "follow_up_needed": True,
            "timestamp": datetime.now().isoformat(),
            "original_question": "How does Promote work with damaged characters?"
        },
        {
            "question_type": "game_zones",
            "keywords_involved": ["Permanent"],
            "complexity_level": 4,
            "game_phase": "start_phase",
            "cards_mentioned": [],
            "relevant_rule_sections": ["6.3.3", "5.2"],
            "clarification": "Permanent strategies move to essence area immediately when last counter is removed.",
            "follow_up_needed": False,
            "timestamp": datetime.now().isoformat(),
            "original_question": "If a Permanent strategy loses all counters, when exactly does it leave play?"
        },
        {
            "question_type": "keyword_ability",
            "keywords_involved": ["Rebirth", "Counter", "Expert"],
            "complexity_level": 5,
            "game_phase": "any_phase",
            "cards_mentioned": [],
            "relevant_rule_sections": ["7.1.7", "7.1.4", "7.1.6", "4.2"],
            "clarification": "Complex chain resolution. Expert effects cannot be countered. Rebirth triggers after destruction.",
            "follow_up_needed": True,
            "timestamp": datetime.now().isoformat(),
            "original_question": "Player A has Rebirth character, Player B destroys it, Player A counters, Player B uses Expert. How does this resolve?"
        }
    ]
    
    # Save test data
    with open("test_primal_questions.json", 'w') as f:
        json.dump(example_parsed_questions, f, indent=2)
    
    print("Sample parsed questions saved to: test_primal_questions.json\n")
    
    # Analyze patterns
    print("ANALYTICS SUMMARY")
    print("-" * 40)
    
    # Question type distribution
    question_types = {}
    for q in example_parsed_questions:
        q_type = q['question_type']
        question_types[q_type] = question_types.get(q_type, 0) + 1
    
    print("Question Type Distribution:")
    for q_type, count in question_types.items():
        percentage = (count / len(example_parsed_questions)) * 100
        print("  - {}: {} ({:.1f}%)".format(q_type, count, percentage))
    
    # Keyword frequency
    keyword_freq = {}
    for q in example_parsed_questions:
        for keyword in q['keywords_involved']:
            keyword_freq[keyword] = keyword_freq.get(keyword, 0) + 1
    
    print("\nMost Common Keywords:")
    for keyword, count in sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)[:5]:
        print("  - {}: {} occurrences".format(keyword, count))
    
    # Complexity analysis
    complexities = [q['complexity_level'] for q in example_parsed_questions]
    avg_complexity = sum(complexities) / len(complexities)
    
    print("\nComplexity Analysis:")
    print("  - Average: {:.1f}/5".format(avg_complexity))
    print("  - Range: {}-{}".format(min(complexities), max(complexities)))
    
    # High complexity topics
    high_complexity = [q for q in example_parsed_questions if q['complexity_level'] >= 4]
    print("\nHigh Complexity Topics ({} questions):".format(len(high_complexity)))
    for q in high_complexity:
        keywords = ", ".join(q['keywords_involved'])
        print("  - {}: {}".format(q['question_type'], keywords))
    
    # Game phase distribution
    phase_dist = {}
    for q in example_parsed_questions:
        phase = q['game_phase']
        phase_dist[phase] = phase_dist.get(phase, 0) + 1
    
    print("\nGame Phase Distribution:")
    for phase, count in phase_dist.items():
        print("  - {}: {}".format(phase, count))
    
    print("\n" + "=" * 50)
    print("EXAMPLE COMPLEX INTERACTION ANALYSIS")
    print("=" * 50)
    
    example_analysis = {
        "scenario": "Player A has a character with Rebirth. Player B destroys it, Player A counters, Player B uses Expert ability.",
        "cards_and_effects": """
Card: Character with Rebirth
Effect: When this character is destroyed, it returns to play

Card: Destruction ability
Effect: Destroys target character

Card: Counter strategy
Effect: Negates the previous effect on the chain

Card: Expert ability
Effect: Cannot be countered, destroys target character
        """,
        "timing_analysis": """
1. Player B activates destruction ability (goes on chain)
2. Priority passes to Player A
3. Player A activates Counter strategy (goes on chain)
4. Priority passes to Player B
5. Player B activates Expert ability (goes on chain)
6. Both players pass priority

Resolution (reverse order):
1. Expert ability resolves first - destroys character (cannot be countered)
2. Counter strategy attempts to resolve - has no effect on Expert
3. Original destruction ability would resolve but target is already destroyed
        """,
        "rules_application": """
Key Rules Applied:
- Rule 7.1.6 (Expert): Expert effects cannot be countered
- Rule 1.2 (Can't beats Can): The "cannot be countered" takes precedence
- Rule 4.2 (Chains): Effects resolve in reverse order
- Rule 7.1.7 (Rebirth): Triggers when character is destroyed

Final Ruling: The character is destroyed by the Expert ability. Rebirth triggers.
        """,
        "educational_summary": """
ANSWER: The character is destroyed by the Expert ability and Rebirth triggers.

KEY RULE: Expert effects cannot be countered (Rule 7.1.6)

TIP: Remember chains resolve backwards - last effect on the chain resolves first!

REVIEW: Section 4.2 (Chains) and 7.1.6 (Expert keyword)
        """
    }
    
    print("Scenario: {}\n".format(example_analysis['scenario']))
    print("Step-by-Step Analysis:")
    print("-" * 40)
    print("1. CARDS AND EFFECTS IDENTIFIED:")
    print(example_analysis['cards_and_effects'])
    print("\n2. TIMING AND PRIORITY:")
    print(example_analysis['timing_analysis'])
    print("\n3. RULES APPLICATION:")
    print(example_analysis['rules_application'])
    print("\n4. EDUCATIONAL SUMMARY:")
    print(example_analysis['educational_summary'])
    
    print("\n" + "=" * 50)
    print("TEST COMPLETE!")
    print("=" * 50)
    print("\nThis test demonstrates the system's ability to:")
    print("1. Parse rules questions into structured data")
    print("2. Track question patterns and analytics")
    print("3. Analyze complex card interactions step-by-step")
    print("4. Generate educational summaries for players")
    print("\nTo run with actual OpenAI API:")
    print("1. Add your OPENAI_API_KEY to .env file")
    print("2. Run: python primal_tcg_rules_assistant.py")

if __name__ == "__main__":
    test_without_api()