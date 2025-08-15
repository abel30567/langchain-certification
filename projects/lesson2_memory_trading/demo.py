#!/usr/bin/env python
"""
Demo script for Primal TCG Trading Assistant
Demonstrates different memory types and trading conversations
"""

import os
from datetime import datetime
from trading_assistant import PrimalTCGTradingAssistant


def demo_conversation_buffer_memory():
    """Demo using ConversationBufferMemory - remembers everything"""
    print("\n" + "="*60)
    print("DEMO 1: ConversationBufferMemory (Full History)")
    print("="*60)
    
    assistant = PrimalTCGTradingAssistant(memory_type="buffer")
    
    # Simulate a trading conversation
    conversations = [
        "Hi, I'm looking to start trading Primal TCG cards. What's hot right now?",
        "Tell me more about Flame Dragon Alpha",
        "What about Shadow Walker? Is it a good investment?",
        "I have $500 to invest. What would you recommend?",
        "Can you analyze a trade of 2 Shadow Walkers for me?",
        "What did we discuss about Flame Dragon Alpha earlier?"
    ]
    
    for user_input in conversations:
        print(f"\n👤 User: {user_input}")
        response = assistant.chat(user_input)
        print(f"🤖 Assistant: {response}")
    
    # Show memory buffer
    print("\n📝 Full Conversation Memory:")
    print(assistant.get_conversation_summary())
    
    # Save conversation
    save_path = f"conversations/buffer_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    print(f"\n💾 {assistant.save_conversation(save_path)}")
    
    return assistant


def demo_conversation_window_memory():
    """Demo using ConversationBufferWindowMemory - remembers last k exchanges"""
    print("\n" + "="*60)
    print("DEMO 2: ConversationBufferWindowMemory (Last 5 exchanges)")
    print("="*60)
    
    assistant = PrimalTCGTradingAssistant(memory_type="window")
    
    # Longer conversation to show window effect
    conversations = [
        "What's the most expensive card?",
        "Tell me about Ancient Artifact",
        "What about the cheapest cards?",
        "I want to buy some Lightning Strike cards",
        "What's the price trend for Time Warp?",
        "Analyze a trade of 3 Time Warp cards",
        "What did we discuss first?",  # This won't remember the first question
        "What about Time Warp?"  # This should remember
    ]
    
    for i, user_input in enumerate(conversations, 1):
        print(f"\n[Exchange {i}]")
        print(f"👤 User: {user_input}")
        response = assistant.chat(user_input)
        print(f"🤖 Assistant: {response}")
    
    print("\n📝 Window Memory (Last 5 exchanges only):")
    print(assistant.get_conversation_summary())
    
    return assistant


def demo_conversation_summary_memory():
    """Demo using ConversationSummaryMemory - summarizes long conversations"""
    print("\n" + "="*60)
    print("DEMO 3: ConversationSummaryMemory (Summarized History)")
    print("="*60)
    
    assistant = PrimalTCGTradingAssistant(memory_type="summary")
    
    # Long conversation that will be summarized
    conversations = [
        "I'm a new trader. Explain the market to me",
        "What factors affect card prices?",
        "Tell me about legendary cards",
        "I'm interested in Flame Dragon Alpha and Time Warp",
        "Compare their investment potential",
        "I have $1000 budget. Create a portfolio for me",
        "Should I focus on rare or legendary cards?",
        "What's my best strategy for long-term gains?"
    ]
    
    for user_input in conversations:
        print(f"\n👤 User: {user_input}")
        response = assistant.chat(user_input)
        print(f"🤖 Assistant: {response[:200]}...")  # Truncate for display
    
    print("\n📝 Summarized Conversation Memory:")
    print(assistant.get_conversation_summary())
    
    # Save conversation
    save_path = f"conversations/summary_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    print(f"\n💾 {assistant.save_conversation(save_path)}")
    
    return assistant


def demo_trade_analysis():
    """Demo trade analysis features"""
    print("\n" + "="*60)
    print("DEMO 4: Trade Analysis and History")
    print("="*60)
    
    assistant = PrimalTCGTradingAssistant(memory_type="buffer")
    
    # Perform several trade analyses
    trades = [
        ("Flame Dragon Alpha", "buy", 1),
        ("Shadow Walker", "buy", 3),
        ("Lightning Strike", "sell", 10),
        ("Ancient Artifact", "buy", 1)
    ]
    
    for card_name, action, quantity in trades:
        print(f"\n📊 Analyzing {action.upper()} {quantity}x {card_name}:")
        analysis = assistant.analyze_trade(card_name, action, quantity)
        print(analysis)
    
    # Show trade history
    print("\n📈 Trade History Summary:")
    for i, trade in enumerate(assistant.get_trade_history(), 1):
        print(f"\n{i}. {trade['card']} - {trade['action'].upper()} {trade['quantity']}x @ ${trade['price']}")
        print(f"   Time: {trade['timestamp']}")
    
    return assistant


def demo_save_load_conversation():
    """Demo saving and loading conversations"""
    print("\n" + "="*60)
    print("DEMO 5: Save and Load Conversations")
    print("="*60)
    
    # Create and save a conversation
    assistant1 = PrimalTCGTradingAssistant(memory_type="buffer")
    
    print("Creating initial conversation...")
    conversations = [
        "I want to invest in mythic cards",
        "Tell me about Ancient Artifact",
        "Is it worth buying now?"
    ]
    
    for user_input in conversations:
        print(f"👤 User: {user_input}")
        response = assistant1.chat(user_input)
        print(f"🤖 Assistant: {response[:100]}...")
    
    # Save conversation
    save_path = "conversations/demo_save_load.json"
    print(f"\n💾 {assistant1.save_conversation(save_path)}")
    
    # Create new assistant and load conversation
    print("\n🔄 Creating new assistant and loading conversation...")
    assistant2 = PrimalTCGTradingAssistant(memory_type="buffer")
    print(assistant2.load_conversation(save_path))
    
    # Continue conversation with loaded memory
    print("\n📖 Continuing conversation with loaded memory:")
    user_input = "What were we discussing about mythic cards?"
    print(f"👤 User: {user_input}")
    response = assistant2.chat(user_input)
    print(f"🤖 Assistant: {response}")
    
    return assistant2


def main():
    """Run all demos"""
    print("\n" + "🎮"*30)
    print("  PRIMAL TCG TRADING ASSISTANT - MEMORY DEMOS")
    print("🎮"*30)
    
    # Run demos
    demos = [
        ("ConversationBufferMemory", demo_conversation_buffer_memory),
        ("ConversationWindowMemory", demo_conversation_window_memory),
        ("ConversationSummaryMemory", demo_conversation_summary_memory),
        ("Trade Analysis", demo_trade_analysis),
        ("Save/Load Conversations", demo_save_load_conversation)
    ]
    
    for demo_name, demo_func in demos:
        input(f"\n\nPress Enter to run {demo_name} demo...")
        demo_func()
    
    print("\n" + "="*60)
    print("✅ All demos completed!")
    print("="*60)
    print("\nKey Takeaways:")
    print("1. ConversationBufferMemory - Keeps entire conversation history")
    print("2. ConversationWindowMemory - Keeps only last k exchanges")
    print("3. ConversationSummaryMemory - Summarizes long conversations")
    print("4. Trade Analysis - Tracks and analyzes trading decisions")
    print("5. Save/Load - Persist conversations for later use")


if __name__ == "__main__":
    main()