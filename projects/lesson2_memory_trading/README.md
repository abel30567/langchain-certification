# Lesson 2 Project: Memory Trading Assistant

A trading assistant that uses LangChain's memory capabilities to maintain context across conversations about trading strategies and market analysis.

## Overview

This project demonstrates how to build a conversational trading assistant that remembers previous interactions, allowing for more contextual and personalized trading advice.

## Features

- **Persistent Conversation Memory**: Maintains context across multiple interactions
- **Trading Context Awareness**: Remembers user's trading preferences and past discussions
- **Market Analysis with Memory**: Builds upon previous analyses in conversations
- **Position Tracking**: Remembers discussed positions and strategies

## Key Components

### Memory Implementation
- Uses ConversationBufferMemory for full conversation history
- Implements memory pruning strategies for long conversations
- Demonstrates memory persistence across sessions

### Trading Features
- Market sentiment analysis with historical context
- Portfolio recommendations based on conversation history
- Risk assessment considering previously discussed factors

## Technologies Used

- LangChain for memory management
- OpenAI GPT models for conversation
- Python for backend implementation

## Getting Started

1. Install dependencies:
   ```bash
   pip install langchain openai python-dotenv
   ```

2. Set up your environment variables in `.env`:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. Run the trading assistant:
   ```bash
   python main.py
   ```

## Use Cases

- Interactive trading strategy discussions
- Market analysis with contextual follow-ups
- Portfolio review with historical context
- Risk management conversations

## Learning Outcomes

- Implement conversation memory in LangChain
- Build context-aware applications
- Manage memory for optimal performance
- Create persistent conversation experiences