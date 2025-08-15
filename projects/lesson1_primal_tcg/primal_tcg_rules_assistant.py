#!/usr/bin/env python
"""
Primal TCG Rules Assistant
A LangChain-based system for clarifying Primal TCG rules and tracking player questions.
Based on lessons from L1-Model_prompt_parser.py
"""

import os
import json
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# Try to find .env file in multiple locations
# First check current directory, then parent directories
env_path = find_dotenv()
if not env_path:
    # Try project root (2 levels up from projects/lesson1_primal_tcg/)
    project_root = Path(__file__).parent.parent.parent
    env_file = project_root / '.env'
    if env_file.exists():
        env_path = str(env_file)
    else:
        # Try current working directory
        env_file = Path.cwd() / '.env'
        if env_file.exists():
            env_path = str(env_file)

# Load environment variables
if env_path:
    load_dotenv(env_path)
    print(f"Loaded .env from: {env_path}")
else:
    print("No .env file found. Checking environment variables...")

# Ensure OpenAI API key is set
if 'OPENAI_API_KEY' not in os.environ:
    print("\n" + "="*50)
    print("WARNING: OPENAI_API_KEY not found!")
    print("="*50)
    print("\nTo use this script, you need to:")
    print("1. Create a .env file in one of these locations:")
    print("   - Current directory")
    print("   - Project root (langchain-certification/)")
    print("   - This script's directory")
    print("\n2. Add your OpenAI API key to the .env file:")
    print("   OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE")
    print("\n3. Get an API key from: https://platform.openai.com/api-keys")
    print("="*50)

# Import LangChain components
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

# ========================
# PART 1: BASIC RULES CLARIFICATION (Simple Prompt Engineering)
# ========================

def initialize_chat(temperature=0.0, model="gpt-3.5-turbo"):
    """Initialize the chat model with specified parameters."""
    return ChatOpenAI(temperature=temperature, model=model)

def create_basic_rules_clarifier():
    """
    Create a basic rules clarification system using simple prompt engineering.
    This demonstrates direct API usage through LangChain.
    """
    
    # Initialize the chat model
    chat = initialize_chat(temperature=0.0)
    
    # Create the prompt template for rules clarification
    template_string = """You are a Primal TCG rules expert. You have access to the comprehensive rules document.
    
    A player is asking about a rules interaction or clarification.
    
    Key Primal TCG concepts to remember:
    - Cards can be In Play (Kingdom, Battlefield, Field) or not In Play
    - Priority and Chains determine when effects resolve
    - "Can't beats can" - negative effects override positive ones
    - "Do as much as you can" rule applies unless "and if you do" clause exists
    - Keywords include: Transformation, Camouflage, Unique, Counter, Permanent, Expert, Rebirth, Promote, Rush
    
    Player Question: {question}
    
    Game State (if provided): {game_state}
    
    Please provide a clear, concise rules clarification. Reference specific rule sections when applicable.
    Format your response in a helpful, educational manner."""
    
    prompt_template = ChatPromptTemplate.from_template(template_string)
    
    def clarify_rule(question: str, game_state: str = "Not specified") -> str:
        """
        Clarify a rules question for a player.
        
        Args:
            question: The player's rules question
            game_state: Optional description of the current game state
            
        Returns:
            A clear rules clarification
        """
        messages = prompt_template.format_messages(
            question=question,
            game_state=game_state
        )
        response = chat(messages)
        return response.content
    
    return clarify_rule

# ========================
# PART 2: STRUCTURED OUTPUT PARSING
# ========================

def create_structured_rules_parser():
    """
    Create a rules parser that outputs structured JSON data for analytics.
    This demonstrates the use of output parsers from the lesson.
    """
    
    chat = initialize_chat(temperature=0.0)
    
    # Define the response schemas for structured output
    question_type_schema = ResponseSchema(
        name="question_type",
        description="The type of rules question. Options: 'keyword_ability', 'card_interaction', 'timing_priority', 'game_zones', 'combat', 'costs_requirements', 'general_mechanic'"
    )
    
    keywords_involved_schema = ResponseSchema(
        name="keywords_involved",
        description="List of keyword abilities involved in the question (e.g., ['Transformation', 'Rush']). Output as a Python list."
    )
    
    complexity_schema = ResponseSchema(
        name="complexity_level",
        description="How complex is this rules question? Rate 1-5 where 1 is basic and 5 is very complex."
    )
    
    game_phase_schema = ResponseSchema(
        name="game_phase",
        description="Which game phase does this question relate to? Options: 'setup', 'start_phase', 'main_phase', 'organization_phase', 'battle_phase', 'end_phase', 'any_phase'"
    )
    
    cards_mentioned_schema = ResponseSchema(
        name="cards_mentioned",
        description="List of specific card names mentioned in the question. Output as a Python list."
    )
    
    rule_sections_schema = ResponseSchema(
        name="relevant_rule_sections",
        description="List of rule sections that apply to this question (e.g., ['1.2', '4.1', '7.1.1']). Output as a Python list."
    )
    
    clarification_schema = ResponseSchema(
        name="clarification",
        description="The actual rules clarification answer to the player's question."
    )
    
    follow_up_needed_schema = ResponseSchema(
        name="follow_up_needed",
        description="Does this question require follow-up information? Answer True or False."
    )
    
    response_schemas = [
        question_type_schema,
        keywords_involved_schema,
        complexity_schema,
        game_phase_schema,
        cards_mentioned_schema,
        rule_sections_schema,
        clarification_schema,
        follow_up_needed_schema
    ]
    
    # Create the output parser
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    
    # Create the prompt template with format instructions
    template = """You are a Primal TCG rules expert analyzing a player's question.
    
    Extract and provide the following information about this rules question:
    
    Player Question: {question}
    
    Game Context: {context}
    
    {format_instructions}
    
    Remember:
    - Be precise in categorizing the question type
    - List all relevant keywords and card names
    - Provide a clear, accurate clarification
    - Reference specific rule sections when applicable
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    
    def parse_rules_question(question: str, context: str = "No specific context provided") -> Dict:
        """
        Parse a rules question into structured data.
        
        Args:
            question: The player's rules question
            context: Optional game context
            
        Returns:
            Structured dictionary with parsed information
        """
        messages = prompt.format_messages(
            question=question,
            context=context,
            format_instructions=format_instructions
        )
        
        response = chat(messages)
        parsed_output = output_parser.parse(response.content)
        
        # Add metadata
        parsed_output['timestamp'] = datetime.now().isoformat()
        parsed_output['original_question'] = question
        
        return parsed_output
    
    return parse_rules_question

# ========================
# PART 3: CHAINED PROMPTS FOR COMPLEX INTERACTIONS
# ========================

def create_complex_interaction_analyzer():
    """
    Create a system that uses multiple chained prompts to analyze complex card interactions.
    This demonstrates prompt chaining for sophisticated analysis.
    """
    
    chat = initialize_chat(temperature=0.0)
    
    # Step 1: Identify the cards and effects involved
    identify_template = """Analyze this Primal TCG scenario and identify all cards and effects involved.
    
    Scenario: {scenario}
    
    List each card mentioned and their relevant effects.
    Format as:
    Card: [card name]
    Effect: [brief description of relevant effect]
    
    If no specific cards are named, identify the types of effects being discussed."""
    
    # Step 2: Determine the timing and priority
    timing_template = """Given these cards and effects in Primal TCG:
    {cards_and_effects}
    
    Original scenario: {scenario}
    
    Determine:
    1. The order in which these effects would go on the chain
    2. How priority passes between players
    3. The resolution order (remember: chains resolve in reverse order)
    
    Format your response clearly with numbered steps."""
    
    # Step 3: Apply relevant rules
    rules_template = """Based on this Primal TCG interaction analysis:
    
    Cards/Effects: {cards_and_effects}
    Timing/Priority: {timing_analysis}
    Original Question: {scenario}
    
    Apply the relevant rules:
    - Check for "can't beats can" situations
    - Apply "do as much as you can" rule if needed
    - Consider any keyword abilities (Transformation, Counter, etc.)
    - Note any special timing rules
    
    Provide the final ruling and explanation."""
    
    # Step 4: Generate educational summary
    summary_template = """Create an educational summary for this Primal TCG rules interaction.
    
    Full Analysis:
    {full_analysis}
    
    Create a response that:
    1. States the final answer clearly
    2. Explains the key rule(s) that apply
    3. Provides a memorable tip for similar situations
    4. Suggests what section of the rulebook to review
    
    Keep it concise but educational."""
    
    identify_prompt = ChatPromptTemplate.from_template(identify_template)
    timing_prompt = ChatPromptTemplate.from_template(timing_template)
    rules_prompt = ChatPromptTemplate.from_template(rules_template)
    summary_prompt = ChatPromptTemplate.from_template(summary_template)
    
    def analyze_complex_interaction(scenario: str) -> Dict[str, str]:
        """
        Analyze a complex card interaction using chained prompts.
        
        Args:
            scenario: Description of the complex interaction
            
        Returns:
            Dictionary with step-by-step analysis and final ruling
        """
        # Step 1: Identify cards and effects
        identify_messages = identify_prompt.format_messages(scenario=scenario)
        cards_and_effects = chat(identify_messages).content
        
        # Step 2: Analyze timing and priority
        timing_messages = timing_prompt.format_messages(
            cards_and_effects=cards_and_effects,
            scenario=scenario
        )
        timing_analysis = chat(timing_messages).content
        
        # Step 3: Apply rules
        rules_messages = rules_prompt.format_messages(
            cards_and_effects=cards_and_effects,
            timing_analysis=timing_analysis,
            scenario=scenario
        )
        rules_application = chat(rules_messages).content
        
        # Step 4: Create summary
        full_analysis = f"""
        Cards/Effects Identified:
        {cards_and_effects}
        
        Timing Analysis:
        {timing_analysis}
        
        Rules Application:
        {rules_application}
        """
        
        summary_messages = summary_prompt.format_messages(full_analysis=full_analysis)
        educational_summary = chat(summary_messages).content
        
        return {
            "scenario": scenario,
            "cards_and_effects": cards_and_effects,
            "timing_analysis": timing_analysis,
            "rules_application": rules_application,
            "educational_summary": educational_summary,
            "timestamp": datetime.now().isoformat()
        }
    
    return analyze_complex_interaction

# ========================
# PART 4: ANALYTICS AND PATTERN TRACKING
# ========================

class RulesQuestionAnalytics:
    """Track and analyze patterns in rules questions."""
    
    def __init__(self, storage_file="primal_tcg_questions.json"):
        self.storage_file = storage_file
        self.questions_data = self.load_data()
        self.chat = initialize_chat(temperature=0.0)
    
    def load_data(self) -> List[Dict]:
        """Load existing question data from file."""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_data(self):
        """Save question data to file."""
        with open(self.storage_file, 'w') as f:
            json.dump(self.questions_data, f, indent=2)
    
    def add_question(self, parsed_question: Dict):
        """Add a parsed question to the analytics data."""
        self.questions_data.append(parsed_question)
        self.save_data()
    
    def analyze_patterns(self) -> Dict:
        """Analyze patterns in the collected questions."""
        if not self.questions_data:
            return {"message": "No data collected yet"}
        
        # Analyze question types
        question_types = {}
        keywords_frequency = {}
        complexity_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        game_phases = {}
        
        for question in self.questions_data:
            # Count question types
            q_type = question.get('question_type', 'unknown')
            question_types[q_type] = question_types.get(q_type, 0) + 1
            
            # Count keyword frequencies
            for keyword in question.get('keywords_involved', []):
                keywords_frequency[keyword] = keywords_frequency.get(keyword, 0) + 1
            
            # Track complexity
            complexity = question.get('complexity_level', 3)
            if complexity in complexity_distribution:
                complexity_distribution[complexity] += 1
            
            # Track game phases
            phase = question.get('game_phase', 'unknown')
            game_phases[phase] = game_phases.get(phase, 0) + 1
        
        # Calculate averages and identify problem areas
        total_questions = len(self.questions_data)
        # Ensure complexity_level is an integer
        complexity_values = []
        for q in self.questions_data:
            comp = q.get('complexity_level', 3)
            if isinstance(comp, str):
                try:
                    comp = int(comp)
                except ValueError:
                    comp = 3  # Default if conversion fails
            complexity_values.append(comp)
        avg_complexity = sum(complexity_values) / total_questions if total_questions > 0 else 0
        
        # Identify most confusing rules
        high_complexity_questions = []
        for q in self.questions_data:
            comp = q.get('complexity_level', 0)
            if isinstance(comp, str):
                try:
                    comp = int(comp)
                except ValueError:
                    comp = 0
            if comp >= 4:
                high_complexity_questions.append(q)
        
        return {
            "total_questions_analyzed": total_questions,
            "question_type_distribution": question_types,
            "most_common_keywords": dict(sorted(keywords_frequency.items(), key=lambda x: x[1], reverse=True)[:5]),
            "average_complexity": round(avg_complexity, 2),
            "complexity_distribution": complexity_distribution,
            "game_phase_distribution": game_phases,
            "high_complexity_topics": self._extract_topics(high_complexity_questions),
            "recommendations": self._generate_recommendations(question_types, keywords_frequency, avg_complexity)
        }
    
    def _extract_topics(self, questions: List[Dict]) -> List[str]:
        """Extract common topics from high-complexity questions."""
        topics = set()
        for q in questions[:5]:  # Top 5 most complex
            topics.add(q.get('question_type', 'unknown'))
            for keyword in q.get('keywords_involved', []):
                topics.add(f"Keyword: {keyword}")
        return list(topics)
    
    def _generate_recommendations(self, question_types: Dict, keywords: Dict, avg_complexity: float) -> List[str]:
        """Generate recommendations based on analytics."""
        recommendations = []
        
        # Check for commonly confusing question types
        if question_types:
            most_common = max(question_types, key=question_types.get)
            recommendations.append(f"Consider creating a guide for '{most_common}' questions (most frequent)")
        
        # Check for problematic keywords
        if keywords:
            most_confusing_keyword = max(keywords, key=keywords.get)
            recommendations.append(f"'{most_confusing_keyword}' ability causes the most confusion")
        
        # Complexity recommendations
        if avg_complexity > 3.5:
            recommendations.append("High average complexity - consider simplifying rule explanations")
        
        return recommendations
    
    def generate_report(self) -> str:
        """Generate a formatted analytics report."""
        analysis = self.analyze_patterns()
        
        if "message" in analysis:
            return analysis["message"]
        
        report = f"""
=== PRIMAL TCG RULES QUESTION ANALYTICS REPORT ===
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY
-------
Total Questions Analyzed: {analysis['total_questions_analyzed']}
Average Complexity: {analysis['average_complexity']}/5

QUESTION TYPES
--------------
"""
        for q_type, count in analysis['question_type_distribution'].items():
            percentage = (count / analysis['total_questions_analyzed']) * 100
            report += f"  • {q_type}: {count} ({percentage:.1f}%)\n"
        
        report += """
MOST CONFUSING KEYWORDS
-----------------------
"""
        for keyword, count in analysis['most_common_keywords'].items():
            report += f"  • {keyword}: {count} questions\n"
        
        report += """
COMPLEXITY DISTRIBUTION
-----------------------
"""
        for level, count in analysis['complexity_distribution'].items():
            report += f"  Level {level}: {'█' * count} ({count})\n"
        
        report += """
HIGH COMPLEXITY TOPICS
----------------------
"""
        for topic in analysis['high_complexity_topics']:
            report += f"  • {topic}\n"
        
        report += """
RECOMMENDATIONS
---------------
"""
        for rec in analysis['recommendations']:
            report += f"  → {rec}\n"
        
        return report

# ========================
# PART 5: EXAMPLE USAGE AND TESTING
# ========================

def run_examples():
    """Run example scenarios to demonstrate the system."""
    
    print("=== PRIMAL TCG RULES ASSISTANT DEMO ===\n")
    
    # Initialize all components
    basic_clarifier = create_basic_rules_clarifier()
    structured_parser = create_structured_rules_parser()
    complex_analyzer = create_complex_interaction_analyzer()
    analytics = RulesQuestionAnalytics()
    
    # Example 1: Basic Rules Clarification
    print("1. BASIC RULES CLARIFICATION")
    print("-" * 40)
    question1 = "Can I use Rush ability if my character was summoned this turn?"
    answer1 = basic_clarifier(question1)
    print(f"Q: {question1}")
    print(f"A: {answer1}\n")
    
    # Example 2: Structured Output Parsing
    print("2. STRUCTURED OUTPUT PARSING")
    print("-" * 40)
    question2 = "If I have a character with Transformation and my opponent uses Counter on it, what happens?"
    parsed2 = structured_parser(question2)
    print(f"Q: {question2}")
    print(f"Parsed Data:")
    print(f"  - Type: {parsed2.get('question_type')}")
    print(f"  - Keywords: {parsed2.get('keywords_involved')}")
    print(f"  - Complexity: {parsed2.get('complexity_level')}/5")
    print(f"  - Clarification: {parsed2.get('clarification')[:100]}...\n")
    
    # Save to analytics
    analytics.add_question(parsed2)
    
    # Example 3: Complex Interaction Analysis
    print("3. COMPLEX INTERACTION ANALYSIS")
    print("-" * 40)
    scenario3 = """
    Player A has a character with Rebirth in their Kingdom. 
    Player B plays an ability that would destroy it, but Player A responds with a Counter strategy card. 
    Player B then plays another ability with Expert effect. 
    How does this resolve?
    """
    complex_result = complex_analyzer(scenario3)
    print(f"Scenario: {scenario3.strip()}")
    print(f"\nEducational Summary:")
    print(complex_result['educational_summary'])
    
    # Parse and add to analytics
    parsed3 = structured_parser(scenario3)
    analytics.add_question(parsed3)
    
    # Example 4: More test cases for analytics
    print("\n4. ADDITIONAL TEST CASES")
    print("-" * 40)
    test_questions = [
        "What happens when two Unique characters with the same name are in play?",
        "Can I activate Camouflage during my opponent's turn?",
        "How does Promote work with damaged characters?",
        "If a Permanent strategy loses all counters, when exactly does it leave play?",
        "Can transformation be used on a character that's already transformed?"
    ]
    
    for q in test_questions:
        parsed = structured_parser(q)
        analytics.add_question(parsed)
        print(f"✓ Processed: {q[:50]}...")
    
    # Example 5: Generate Analytics Report
    print("\n5. ANALYTICS REPORT")
    print("-" * 40)
    report = analytics.generate_report()
    print(report)
    
    return analytics

if __name__ == "__main__":
    # Check for API key
    if 'OPENAI_API_KEY' not in os.environ:
        print("ERROR: OpenAI API key not found!")
        print("Please add OPENAI_API_KEY to your .env file")
        print("\nExample .env file:")
        print("OPENAI_API_KEY=your-api-key-here")
    else:
        # Run the examples
        analytics = run_examples()
        
        print("\n" + "=" * 50)
        print("DEMO COMPLETE!")
        print("=" * 50)
        print("\nThis system demonstrates:")
        print("1. Basic prompt engineering for rules clarification")
        print("2. Structured output parsing for data collection")
        print("3. Chained prompts for complex analysis")
        print("4. Analytics tracking for pattern recognition")
        print("\nData saved to: primal_tcg_questions.json")