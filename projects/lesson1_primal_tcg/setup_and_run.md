# Setup Instructions for Primal TCG Rules Assistant

## Prerequisites

1. Python 3.7+ installed
2. OpenAI API key (get one at https://platform.openai.com/api-keys)

## Installation Steps

### 1. Install Required Packages

```bash
pip install python-dotenv openai langchain
```

### 2. Set Up Your API Key

#### Option A: Create .env file (Recommended)
```bash
# Copy the example file
cp .env.example .env

# Edit .env and replace sk-proj-YOUR_API_KEY_HERE with your actual API key
# Example: OPENAI_API_KEY=sk-proj-abc123xyz789...
```

#### Option B: Set Environment Variable
```bash
# On Mac/Linux:
export OPENAI_API_KEY="your-actual-api-key-here"

# On Windows (Command Prompt):
set OPENAI_API_KEY=your-actual-api-key-here

# On Windows (PowerShell):
$env:OPENAI_API_KEY="your-actual-api-key-here"
```

### 3. Run the Assistant

```bash
python primal_tcg_rules_assistant.py
```

## What the System Will Do

When you run the script with a valid API key, it will:

1. **Basic Rules Clarification**: Answer a question about Rush ability
2. **Structured Parsing**: Parse a complex Transformation/Counter interaction
3. **Complex Analysis**: Analyze a multi-step chain with Rebirth, Counter, and Expert
4. **Process Test Questions**: Parse 5 additional rules questions
5. **Generate Analytics Report**: Show patterns in the questions

## Expected Output

```
=== PRIMAL TCG RULES ASSISTANT DEMO ===

1. BASIC RULES CLARIFICATION
----------------------------------------
Q: Can I use Rush ability if my character was summoned this turn?
A: Yes, you can use Rush ability if your character was summoned this turn...

2. STRUCTURED OUTPUT PARSING
----------------------------------------
Q: If I have a character with Transformation and my opponent uses Counter on it, what happens?
Parsed Data:
  - Type: card_interaction
  - Keywords: ['Transformation', 'Counter']
  - Complexity: 4/5
  - Clarification: When Counter is used on Transformation...

[continues with more examples and analytics]
```

## Files Generated

- `primal_tcg_questions.json`: Stores all parsed questions for analytics
- Analytics data persists between runs

## Troubleshooting

### "OPENAI_API_KEY not found in environment"
- Make sure your .env file is in the same directory as the script
- Verify the API key is correctly formatted (starts with sk-)
- Check that python-dotenv is installed

### API Errors
- Verify your API key is active and has credits
- Check OpenAI service status at https://status.openai.com/
- Ensure you're using a supported model (gpt-3.5-turbo or gpt-4)

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade python-dotenv openai langchain
```

## Cost Estimates

Using GPT-3.5-turbo:
- Running the full demo: ~$0.01-0.02
- Each rules question: ~$0.001-0.002

Using GPT-4:
- Running the full demo: ~$0.10-0.20
- Each rules question: ~$0.01-0.02

## Customization

To use a different model, either:
1. Edit the .env file: `OPENAI_MODEL=gpt-4`
2. Or modify the code: `initialize_chat(model="gpt-4")`

## Security Note

**NEVER commit your .env file with real API keys to Git!**

The .gitignore should include:
```
.env
*.json
```