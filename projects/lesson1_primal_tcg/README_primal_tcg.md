# Primal TCG Rules Assistant

A LangChain-based system for clarifying Primal TCG rules and analyzing player questions, built using lessons from the LangChain Models, Prompts, and Output Parsers tutorial.

## Overview

This project demonstrates progressive complexity in using LangChain:
1. **Basic Prompt Engineering** - Simple rules clarification
2. **Structured Output Parsing** - JSON data extraction for analytics
3. **Chained Prompts** - Complex multi-step analysis
4. **Analytics System** - Pattern tracking and insights

## Features

### 1. Basic Rules Clarification
- Direct rules answers using prompt templates
- References comprehensive rules document
- Handles game state context

### 2. Structured Data Extraction
- Parses questions into JSON format
- Categorizes question types
- Identifies keywords and complexity
- Tracks relevant rule sections

### 3. Complex Interaction Analysis
- Multi-step prompt chaining
- Card identification
- Timing/priority analysis
- Rules application
- Educational summaries

### 4. Analytics Dashboard
- Tracks question patterns
- Identifies confusing rules
- Generates reports
- Provides recommendations

## Installation

```bash
# Install dependencies
pip install python-dotenv openai langchain

# Create .env file
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

## Usage

### Run Full Demo (requires OpenAI API key)
```python
python primal_tcg_rules_assistant.py
```

### Run Test Without API
```python
python test_primal_assistant.py
```

### Example Code Usage

```python
from primal_tcg_rules_assistant import *

# Basic clarification
clarifier = create_basic_rules_clarifier()
answer = clarifier("Can I use Rush ability if my character was summoned this turn?")

# Structured parsing
parser = create_structured_rules_parser()
data = parser("What happens with Transformation and Counter?")

# Complex analysis
analyzer = create_complex_interaction_analyzer()
result = analyzer("Player A has Rebirth, Player B destroys it...")

# Analytics
analytics = RulesQuestionAnalytics()
analytics.add_question(data)
report = analytics.generate_report()
```

## Data Structure

Parsed questions are stored with:
- `question_type`: Category of rules question
- `keywords_involved`: List of game keywords
- `complexity_level`: 1-5 difficulty rating
- `game_phase`: Which phase of the game
- `cards_mentioned`: Specific cards referenced
- `relevant_rule_sections`: Applicable rules
- `clarification`: The answer
- `follow_up_needed`: Boolean flag

## Analytics Insights

The system tracks:
- Most common question types
- Frequently confusing keywords
- Complexity distribution
- Problem areas needing documentation
- Recommendations for rule clarifications

## File Structure

```
primal_tcg_rules_assistant.py  # Main system
test_primal_assistant.py       # Test without API
primal_tcg_questions.json      # Stored question data
test_primal_questions.json     # Test data
README_primal_tcg.md           # This file
```

## Key Primal TCG Concepts

- **In Play vs Not In Play**: Kingdom, Battlefield, Field are "In Play"
- **Priority and Chains**: Determine effect resolution order
- **"Can't Beats Can"**: Negative effects override positive
- **"Do as Much as You Can"**: Partial completion rule
- **Keywords**: Transformation, Camouflage, Rush, Rebirth, etc.

## LangChain Concepts Applied

1. **ChatOpenAI**: LLM interface with temperature control
2. **ChatPromptTemplate**: Reusable prompt structures
3. **StructuredOutputParser**: JSON extraction with schemas
4. **ResponseSchema**: Define expected output fields
5. **Prompt Chaining**: Sequential analysis steps
6. **format_messages()**: Template variable injection

## Future Enhancements

- Web interface for rules queries
- Card database integration
- Visual chain resolution diagrams
- Community question voting
- Multi-language support
- Tournament judge assistance mode

## Contributing

To add new features:
1. Extend parser schemas for new data points
2. Add prompt templates for new question types
3. Update analytics to track new patterns
4. Test with example scenarios

## License

Educational project based on Primal TCG Comprehensive Rules v1.3.1