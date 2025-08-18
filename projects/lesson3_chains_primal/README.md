# Lesson 3 Project: Primal TCG Chains System

A comprehensive implementation of LangChain chains for competitive Primal TCG deck analysis, demonstrating SimpleSequentialChain, SequentialChain, RouterChain, and custom chain combinations.

## 🎯 Project Overview

This project demonstrates all major chain concepts from Lesson 3 by building a sophisticated Primal TCG analysis system that can:
- Optimize deck compositions
- Analyze competitive viability
- Identify combos and synergies
- Route questions to specialized experts
- Prepare players for tournaments

## 🏗️ Architecture

### Chain Types Implemented

#### 1. **SimpleSequentialChain** (2-3 chains)
- **Location**: `chains/deck_builder_chain.py`
- **Purpose**: Basic deck analysis flowing into strategy generation
- **Flow**: Deck Analysis → Strategy Guide

#### 2. **SequentialChain** (4-5 chains)
- **Location**: Multiple modules
- **Purpose**: Complex multi-stage analysis with named inputs/outputs
- **Examples**:
  - Deck Optimization: Weakness → Meta → Improvements → Optimization
  - Strategy Analysis: Combos → Game Plan → Counters → Matchups
  - Competitive Analysis: Power → Matchups → Tech → Tournament → Summary

#### 3. **RouterChain** (MultiPromptChain)
- **Location**: `chains/router_chain.py`
- **Purpose**: Routes questions to 7 specialized expert systems
- **Experts**:
  - Rules Expert (game mechanics)
  - Deck Building Expert (optimization)
  - Strategy Expert (gameplay)
  - Meta Expert (tournament trends)
  - Trading Expert (card values)
  - Beginner Expert (new players)
  - Lore Expert (story/flavor)

#### 4. **Custom Competitive Chains**
- **Location**: `chains/competitive_chain.py`
- **Purpose**: Tournament-level analysis combining multiple chain types
- **Features**: 5-stage analysis, head-to-head matchups, tier assessments

## 📁 Project Structure

```
lesson3_chains_primal/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── data/                       # Deck data
│   ├── deck1.json             # Mixed strategy deck (PIRATE/MECHA)
│   ├── deck2.json             # SIN control deck
│   └── deck3.json             # MICROMON combo deck
├── utils/
│   ├── __init__.py
│   └── data_loader.py         # Deck data processing utilities
├── chains/
│   ├── __init__.py
│   ├── deck_builder_chain.py  # SimpleSequentialChain & SequentialChain
│   ├── strategy_chain.py      # Strategy and combo analysis
│   ├── router_chain.py        # MultiPromptChain router
│   └── competitive_chain.py   # Tournament-level analysis
├── demo_interactive.py         # Interactive demonstration
└── demo_automatic.py          # Automatic showcase of all features
```

## 🚀 Getting Started

### Installation

1. Navigate to the project directory:
```bash
cd projects/lesson3_chains_primal
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create .env file in project root
echo "OPENAI_API_KEY=your_key_here" > .env
```

## 🎮 Running the Demos

### Interactive Demo
Allows you to explore each chain type with custom inputs:

```bash
python demo_interactive.py
```

Features:
- Menu-driven interface
- Choose specific chain types to explore
- Select decks for analysis
- Toggle verbose output
- Ask custom questions to the router

### Automatic Demo
Showcases all chain types automatically:

```bash
python demo_automatic.py
```

Features:
- Runs through all chain implementations
- No user input required
- Demonstrates both simple and complex chains
- Shows competitive analysis workflow

## 💡 Key Features

### Priority 1: Deck Building & Optimization
- **SimpleSequentialChain**: Basic deck analysis → strategy guide
- **SequentialChain**: 4-stage optimization process
- Deck comparison and hybrid creation
- Mana curve analysis

### Priority 2: Game Strategy & Combo Analysis
- Combo identification with power ratings
- Turn-by-turn game plans
- Counter-strategy analysis
- Matchup-specific adjustments

### Priority 3: Tournament Preparation
- 5-stage competitive analysis
- Power level assessments (1-10 scales)
- Meta matchup spreads
- Sideboard construction
- Tournament day checklists

## 📊 Chain Complexity Examples

### Simple Example (2-3 chains)
```python
# SimpleSequentialChain in deck_builder_chain.py
Deck Composition Analysis → Strategy Guide Generation
```

### Complex Example (5+ chains)
```python
# Competitive Analysis in competitive_chain.py
Power Assessment → Matchup Analysis → Tech Recommendations → 
Tournament Prep → Executive Summary
```

## 🔍 Competitive Deck Analysis Focus

The system provides comprehensive competitive analysis including:

1. **Deck Power Ratings**
   - Raw power (card quality)
   - Speed (turns to win)
   - Consistency (mulligan reliability)
   - Resilience (disruption recovery)

2. **Meta Positioning**
   - Favorable/unfavorable matchups
   - Win rate predictions
   - Counter-meta adaptations

3. **Tournament Preparation**
   - Practice schedules
   - Sideboard guides
   - Mental notes sheets
   - Energy management tips

## 📈 Data Integration

The project uses real Primal TCG deck data with:
- Complete card effects and rulings
- Turn costs and ability costs
- Card types (Field, Character, Ability, Strategy)
- Skills/archetypes (PIRATE, SIN, MICROMON, etc.)
- Leader/Support values for combat

## 🎯 Learning Outcomes

This project demonstrates:
1. **Chain Selection**: When to use each chain type
2. **Chain Composition**: Building complex workflows
3. **Error Handling**: Managing token limits and edge cases
4. **Domain Application**: Applying chains to real-world problems
5. **User Experience**: Both interactive and automatic demonstrations

## 🔧 Customization

To add your own decks:
1. Place deck JSON files in the `data/` directory
2. Follow the existing deck structure format
3. The system will automatically detect and load them

To add new expert types to the router:
1. Edit `chains/router_chain.py`
2. Add new template in `_create_expert_templates()`
3. The router will automatically include it

## 📝 Example Outputs

### Simple Sequential Chain
```
Input: Deck composition analysis
Output: Complete strategy guide with mulligan decisions, 
        game plans, and win conditions
```

### Router Chain
```
Question: "How does TRIGGER stacking work?"
Routes to: Rules Expert
Response: Detailed rules explanation with timing
```

### Competitive Analysis
```
Input: Deck data
Output: Tier placement, matchup spread, tech recommendations,
        tournament guide, executive summary
```

## 🤝 Acknowledgments

- Built as part of the LangChain for LLM Application Development course
- Uses Primal TCG (https://primaltcg.com) as the domain
- Demonstrates concepts from Lesson 3: Chains

## 📚 Related Lessons

- **Lesson 1**: Models, Prompts, and Parsers
- **Lesson 2**: Memory
- **Lesson 3**: Chains (this project)
- **Lesson 4**: Question and Answer (upcoming)

---

*This project showcases both simple and complex chain implementations for competitive TCG analysis, fulfilling all requirements for demonstrating chain concepts in a practical, domain-specific application.*