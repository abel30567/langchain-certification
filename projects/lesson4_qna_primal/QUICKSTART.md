# Quick Start Guide - Primal TCG Q&A System

## 1-Minute Setup

```bash
# Run setup script
./setup.sh

# Add your OpenAI API key to .env
nano .env  # or use any text editor

# Run a demo
python demo_interactive.py
```

## What This System Does

Ask questions about Primal TCG and get intelligent answers from:
- **Card Database**: 1000+ cards with effects, costs, and attributes
- **Rules Document**: Complete game rules and mechanics
- **Deck Examples**: Competitive deck compositions

## Interactive Demo Options

### 1. Deck Building Mode
```
"What cards work well with Synthetic Laboratory?"
"Build me a Fire/Air aggro deck"
"Suggest TRIGGER ability synergies"
```

### 2. Card Search Mode
```
"Show all Fire cards under 3 cost"
"List cards with REBIRTH ability"
"Find all Synthetic Life creatures"
```

### 3. Rules Mode
```
"How does TRIGGER stacking work?"
"Explain the combat phase"
"When can I activate abilities?"
```

### 4. Comparison Mode
```
"Compare Fire vs Air for aggro strategies"
"Which is better: TRIGGER or ACTIVATE?"
"Compare BIO vs PLEAGUIS attributes"
```

### 5. Free Query Mode
Ask anything - system auto-detects query type!

### 6. Conversational Mode
Have a multi-turn conversation about deck building with memory.

## Automatic Demo

See everything in action without interaction:
```bash
python demo_automatic.py
```

Shows:
- Document retrieval strategies
- Different QA chain types
- Advanced retrieval (MMR, hybrid)
- Conversational Q&A with memory
- Performance comparisons

## Key Features

- **Smart Query Routing**: Automatically uses the right chain for your question
- **Multiple Retrieval Strategies**: Similarity, MMR, hybrid search
- **Rich Metadata**: Filter by card type, cost, element, etc.
- **Conversational Memory**: Build decks iteratively
- **Formatted Responses**: Tables for cards, structured text for rules

## Example Session

```python
# Interactive mode
>>> "Build a TRIGGER-focused deck"

Answer:
For a TRIGGER-focused deck, consider:

Core Cards:
- X-SL0: TRIGGER on play, adds resources
- Benzin: TRIGGER on attack, reduces enemy stats
- X-SL11: TRIGGER from deck, provides recursion

Synergies:
- Synthetic Laboratory field card enhances TRIGGER effects
- Chain multiple TRIGGER abilities for combo plays

Mana Curve:
- 0-1 cost: 8 cards (early TRIGGERS)
- 2-3 cost: 12 cards (development)
- 4+ cost: 5 cards (finishers)

[Based on 4 sources: 3 cards, 1 deck analysis]
```

## Troubleshooting

**"No module named 'langchain'"**
- Run: `pip install -r requirements.txt`

**"OPENAI_API_KEY not found"**
- Edit `.env` file with your API key

**Slow responses**
- Normal for first run (building embeddings)
- Subsequent queries are faster

## Advanced Usage

### Test Different Retrievers
Option 7 in interactive mode compares:
- Similarity search
- MMR (diverse results)
- Hybrid (multi-source)

### Custom Queries
Combine multiple aspects:
```
"Compare Fire and Air TRIGGER cards under 3 cost for an aggro Synthetic Laboratory deck"
```

## Files and Data

- `data/cards.csv`: Complete card database
- `data/rules.md`: Game rules document
- `data/deck*.json`: Sample competitive decks
- `demo_interactive.py`: Interactive Q&A interface
- `demo_automatic.py`: Automated demonstration