#!/usr/bin/env python
"""
Primal TCG Trading Assistant with Memory
Uses LangChain memory components to track trading conversations and market analysis
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional

from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import (
    ConversationBufferMemory,
    ConversationSummaryMemory,
    ConversationBufferWindowMemory,
    CombinedMemory
)
from langchain.prompts import PromptTemplate
from langchain.schema import BaseMessage
import warnings

warnings.filterwarnings('ignore')

_ = load_dotenv(find_dotenv())


class PrimalTCGTradingAssistant:
    """Trading assistant for Primal TCG with conversation memory"""
    
    def __init__(self, memory_type: str = "buffer", llm_model: str = "gpt-3.5-turbo"):
        """
        Initialize the trading assistant
        
        Args:
            memory_type: Type of memory to use ("buffer", "summary", "window", "combined")
            llm_model: The LLM model to use
        """
        self.llm = ChatOpenAI(temperature=0.3, model=llm_model)
        self.memory_type = memory_type
        self.cards_data = self._load_card_data()
        self.trade_history = []
        
        # Initialize memory based on type
        self.memory = self._initialize_memory(memory_type)
        
        # Create custom prompt for trading assistant
        self.prompt_template = PromptTemplate(
            input_variables=["history", "input"],
            template="""You are a knowledgeable Primal TCG trading assistant. 
            You help users make informed trading decisions based on market data and card values.
            You remember previous conversations and can track trading patterns.
            
            Available card data and market trends are provided to you.
            Always consider market trends, supply/demand, and price history when giving advice.
            
            Previous conversation:
            {history}
            
            Human: {input}
            Trading Assistant:"""
        )
        
        # Create conversation chain
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=self.prompt_template,
            verbose=False
        )
        
        # Inject initial context about available cards
        self._inject_initial_context()
    
    def _load_card_data(self) -> Dict:
        """Load mock card data"""
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'mock_cards.json')
        with open(data_path, 'r') as f:
            return json.load(f)
    
    def _initialize_memory(self, memory_type: str):
        """Initialize the appropriate memory type"""
        if memory_type == "buffer":
            return ConversationBufferMemory()
        elif memory_type == "summary":
            return ConversationSummaryMemory(llm=self.llm)
        elif memory_type == "window":
            return ConversationBufferWindowMemory(k=5)  # Keep last 5 exchanges
        elif memory_type == "combined":
            # Combine buffer for recent and summary for older conversations
            buffer_memory = ConversationBufferWindowMemory(k=3)
            summary_memory = ConversationSummaryMemory(llm=self.llm)
            return buffer_memory  # For simplicity, using buffer window
        else:
            return ConversationBufferMemory()
    
    def _inject_initial_context(self):
        """Inject initial context about available cards into memory"""
        context = self._generate_market_context()
        self.memory.save_context(
            {"input": "What cards are available for trading?"},
            {"output": context}
        )
    
    def _generate_market_context(self) -> str:
        """Generate current market context"""
        cards = self.cards_data['cards']
        trends = self.cards_data['market_trends']
        recommendations = self.cards_data['trade_recommendations']
        
        context = f"""Current Primal TCG Market Overview:
        
        Total Cards Available: {len(cards)}
        Hot Cards: {', '.join([self._get_card_name(cid) for cid in trends['hot_cards']])}
        Declining Cards: {', '.join([self._get_card_name(cid) for cid in trends['declining']])}
        
        Trading Recommendations:
        - Buy: {', '.join([self._get_card_name(cid) for cid in recommendations['buy']])}
        - Sell: {', '.join([self._get_card_name(cid) for cid in recommendations['sell']])}
        - Hold: {', '.join([self._get_card_name(cid) for cid in recommendations['hold']])}
        """
        return context
    
    def _get_card_name(self, card_id: str) -> str:
        """Get card name by ID"""
        for card in self.cards_data['cards']:
            if card['id'] == card_id:
                return card['name']
        return "Unknown"
    
    def get_card_info(self, card_name: str) -> Optional[Dict]:
        """Get detailed card information"""
        for card in self.cards_data['cards']:
            if card_name.lower() in card['name'].lower():
                return card
        return None
    
    def analyze_trade(self, card_name: str, action: str = "buy", quantity: int = 1) -> str:
        """Analyze a potential trade"""
        card = self.get_card_info(card_name)
        if not card:
            return f"Card '{card_name}' not found in database."
        
        total_value = card['market_price'] * quantity
        price_trend = "increasing" if card['price_history'][-1] > card['price_history'][0] else "stable"
        
        analysis = f"""
        Trade Analysis for {card['name']}:
        - Current Price: ${card['market_price']}
        - Quantity: {quantity}
        - Total Value: ${total_value}
        - Rarity: {card['rarity']}
        - Supply: {card['supply']} units
        - Demand: {card['demand']}
        - Price Trend: {price_trend}
        - Recent Prices: {card['price_history']}
        
        Recommendation: {"Good time to " + action if card['demand'] == 'High' and action == 'buy' else "Consider waiting"}
        """
        
        # Record in trade history
        self.trade_history.append({
            "timestamp": datetime.now().isoformat(),
            "card": card['name'],
            "action": action,
            "quantity": quantity,
            "price": card['market_price'],
            "analysis": analysis
        })
        
        return analysis
    
    def chat(self, user_input: str) -> str:
        """Process user input and return response"""
        # Check if user is asking about specific cards
        for card in self.cards_data['cards']:
            if card['name'].lower() in user_input.lower():
                # Inject card info into context
                card_info = f"Card Info - {card['name']}: Price ${card['market_price']}, Rarity: {card['rarity']}, Demand: {card['demand']}"
                self.conversation.memory.save_context(
                    {"input": "System: Card data update"},
                    {"output": card_info}
                )
        
        # Get response from conversation chain
        response = self.conversation.predict(input=user_input)
        return response
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation"""
        if isinstance(self.memory, ConversationSummaryMemory):
            return self.memory.buffer
        elif hasattr(self.memory, 'buffer'):
            return self.memory.buffer
        else:
            memory_vars = self.memory.load_memory_variables({})
            return memory_vars.get('history', 'No conversation history available')
    
    def get_trade_history(self) -> List[Dict]:
        """Get the trade analysis history"""
        return self.trade_history
    
    def save_conversation(self, filepath: str):
        """Save conversation to file"""
        conversation_data = {
            "timestamp": datetime.now().isoformat(),
            "memory_type": self.memory_type,
            "conversation": self.get_conversation_summary(),
            "trade_history": self.trade_history,
            "memory_variables": self.memory.load_memory_variables({})
        }
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(conversation_data, f, indent=2)
        
        return f"Conversation saved to {filepath}"
    
    def load_conversation(self, filepath: str):
        """Load conversation from file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Restore trade history
        self.trade_history = data.get('trade_history', [])
        
        # Restore memory context
        if 'memory_variables' in data and 'history' in data['memory_variables']:
            # Parse and restore conversation history
            history = data['memory_variables']['history']
            # This is a simplified restoration - in production you'd parse the history properly
            self.memory.clear()
            if history:
                # Extract key conversations and restore them
                lines = history.split('\n')
                for i in range(0, len(lines)-1, 2):
                    if 'Human:' in lines[i] and 'AI:' in lines[i+1]:
                        human_input = lines[i].replace('Human:', '').strip()
                        ai_output = lines[i+1].replace('AI:', '').strip()
                        self.memory.save_context(
                            {"input": human_input},
                            {"output": ai_output}
                        )
        
        return f"Conversation loaded from {filepath}"
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear()
        self.trade_history = []
        self._inject_initial_context()  # Re-inject initial context
        return "Memory cleared. Starting fresh conversation."