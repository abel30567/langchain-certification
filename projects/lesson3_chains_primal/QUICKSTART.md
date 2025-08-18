# Quick Start Guide - Primal TCG Chains Project

## Setup (One-time)

### Option 1: Automatic Setup (Recommended)
```bash
./setup.sh
```

### Option 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "OPENAI_API_KEY=your_key_here" > .env
```

## Running the Demos

### Interactive Demo
Explore each chain type with a menu system:
```bash
python3 demo_interactive.py
```

**What you can do:**
- Test SimpleSequentialChain (Option 1)
- Test Complex SequentialChain (Option 2)
- Test Strategy Analysis (Option 3)
- Ask questions to Router Chain (Option 4)
- Run Competitive Analysis (Option 5)
- Compare decks (Option 6)

### Automatic Demo
See all chains in action automatically:
```bash
python3 demo_automatic.py
```

**What it shows:**
- All 6 chain types
- Both simple and complex implementations
- Competitive deck analysis workflow
- Chain type comparisons

## Test Your Setup
```bash
python3 test_imports.py
```

## Understanding the Chains

### Simple (2-3 chains)
- **SimpleSequentialChain**: Deck Analysis → Strategy Guide

### Complex (5+ chains)
- **Competitive Analysis**: Power → Matchups → Tech → Tournament → Summary
- **Strategy Analysis**: Combos → Game Plan → Counters → Matchups

### Router Chain
- 7 expert systems for different question types
- Automatically routes to the right expert

## Troubleshooting

**"No module named 'langchain'"**
- Make sure you activated the virtual environment
- Run: `source venv/bin/activate`

**"OpenAI API key not found"**
- Edit the `.env` file
- Add your actual API key

**Import errors**
- Run: `pip install -r requirements.txt`

## Key Files to Explore

- `chains/deck_builder_chain.py` - SimpleSequentialChain & SequentialChain
- `chains/router_chain.py` - MultiPromptChain with 7 experts
- `chains/competitive_chain.py` - Complex 5-stage analysis
- `chains/strategy_chain.py` - Combo and game plan analysis

## Next Steps

1. Try the interactive demo first
2. Modify the chains for your own use case
3. Add new expert types to the router
4. Create custom chain combinations