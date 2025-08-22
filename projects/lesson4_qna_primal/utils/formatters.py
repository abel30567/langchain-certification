"""
Formatting utilities for displaying Q&A results
"""

from typing import List, Dict, Any
from tabulate import tabulate
import re


class ResponseFormatter:
    """Format Q&A responses for better readability"""
    
    @staticmethod
    def format_card_table(cards: List[Dict[str, Any]]) -> str:
        """
        Format cards as a markdown table.
        
        Args:
            cards: List of card dictionaries
            
        Returns:
            Markdown formatted table
        """
        if not cards:
            return "No cards found."
        
        # Define table headers
        headers = ["Name", "Type", "Cost", "Elements", "Effect (Preview)", "Rarity"]
        
        # Prepare table data
        table_data = []
        for card in cards:
            name = card.get('name', 'Unknown')
            card_type = card.get('card_type', 'Unknown')
            cost = card.get('cost', 'N/A')
            elements = card.get('elements', 'N/A')
            effect = card.get('effect', 'No effect')[:50] + "..." if len(card.get('effect', '')) > 50 else card.get('effect', 'No effect')
            rarity = card.get('rarity', 'Unknown')
            
            table_data.append([name, card_type, cost, elements, effect, rarity])
        
        # Create table
        return tabulate(table_data, headers=headers, tablefmt="pipe")
    
    @staticmethod
    def format_deck_recommendations(recommendations: Dict[str, Any]) -> str:
        """
        Format deck building recommendations.
        
        Args:
            recommendations: Dictionary of recommendations
            
        Returns:
            Formatted string
        """
        output = []
        
        if 'core_cards' in recommendations:
            output.append("**Core Cards:**")
            for card in recommendations['core_cards']:
                output.append(f"- {card}")
        
        if 'synergies' in recommendations:
            output.append("\n**Key Synergies:**")
            for synergy in recommendations['synergies']:
                output.append(f"- {synergy}")
        
        if 'mana_curve' in recommendations:
            output.append("\n**Mana Curve Suggestions:**")
            output.append(recommendations['mana_curve'])
        
        if 'sideboard' in recommendations:
            output.append("\n**Sideboard Options:**")
            for card in recommendations['sideboard']:
                output.append(f"- {card}")
        
        return "\n".join(output)
    
    @staticmethod
    def extract_cards_from_text(text: str) -> List[Dict[str, str]]:
        """
        Extract card information from text.
        
        Args:
            text: Text containing card information
            
        Returns:
            List of card dictionaries
        """
        cards = []
        
        # Pattern to match card entries
        card_pattern = r"Card Name: ([^\n]+)"
        
        matches = re.findall(card_pattern, text)
        for match in matches:
            cards.append({'name': match})
        
        return cards
    
    @staticmethod
    def format_rules_clarification(rules_text: str) -> str:
        """
        Format rules text for better readability.
        
        Args:
            rules_text: Raw rules text
            
        Returns:
            Formatted rules text
        """
        # Add bullet points for numbered items
        rules_text = re.sub(r'^(\d+\.)', r'• \1', rules_text, flags=re.MULTILINE)
        
        # Bold section headers
        rules_text = re.sub(r'^(#+\s+.+)$', r'**\1**', rules_text, flags=re.MULTILINE)
        
        return rules_text
    
    @staticmethod
    def format_comparison_table(items: List[Dict[str, Any]], attributes: List[str]) -> str:
        """
        Format a comparison table.
        
        Args:
            items: List of items to compare
            attributes: Attributes to compare
            
        Returns:
            Markdown formatted comparison table
        """
        if not items:
            return "No items to compare."
        
        headers = ["Item"] + attributes
        table_data = []
        
        for item in items:
            row = [item.get('name', 'Unknown')]
            for attr in attributes:
                row.append(item.get(attr, 'N/A'))
            table_data.append(row)
        
        return tabulate(table_data, headers=headers, tablefmt="pipe")