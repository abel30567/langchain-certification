"""
Data loader utility for Primal TCG deck analysis
"""
import json
import os
from typing import Dict, List, Any
from collections import Counter

class DeckLoader:
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            # Get the absolute path to the data directory
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.data_dir = os.path.join(current_dir, "data")
        else:
            self.data_dir = data_dir
        self.decks = {}
        self.load_decks()
    
    def load_decks(self):
        """Load all deck JSON files from the data directory"""
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json'):
                with open(os.path.join(self.data_dir, filename), 'r') as f:
                    deck_name = filename.replace('.json', '')
                    self.decks[deck_name] = json.load(f)
    
    def get_deck(self, deck_name: str) -> Dict:
        """Get a specific deck by name"""
        return self.decks.get(deck_name, {})
    
    def analyze_deck_composition(self, deck_name: str) -> Dict[str, Any]:
        """Analyze the composition of a deck"""
        deck_data = self.get_deck(deck_name)
        if not deck_data or 'deck' not in deck_data:
            return {}
        
        deck = deck_data['deck']
        
        # Analyze card types
        card_types = Counter([card.get('cardType', 'Unknown') for card in deck])
        
        # Analyze skills/archetypes
        skills = Counter([card.get('skill', 'None') for card in deck if card.get('skill')])
        
        # Analyze turn costs (mana curve)
        turn_costs = Counter([card.get('turnCount', 0) for card in deck])
        
        # Analyze elements
        elements = []
        for card in deck:
            if 'element' in card:
                elements.extend(card['element'])
        element_distribution = Counter(elements)
        
        # Analyze ability costs
        ability_costs = []
        for card in deck:
            if 'abilityCost' in card and card['abilityCost']:
                ability_costs.extend(card['abilityCost'])
        
        # Count unique ability cost types
        cost_types = set()
        for cost in ability_costs:
            if isinstance(cost, str):
                # Extract letter from cost (e.g., 'F' from 'F1' or just 'F')
                for char in cost:
                    if char in ['T', 'F', 'W', 'S', 'P', 'N', 'A', 'X']:
                        cost_types.add(char)
        
        return {
            'total_cards': len(deck),
            'card_types': dict(card_types),
            'skills': dict(skills),
            'mana_curve': dict(turn_costs),
            'elements': dict(element_distribution),
            'ability_cost_types': list(cost_types),
            'deck_name': deck_name
        }
    
    def get_card_texts(self, deck_name: str) -> List[str]:
        """Extract all card texts from a deck for analysis"""
        deck_data = self.get_deck(deck_name)
        if not deck_data or 'deck' not in deck_data:
            return []
        
        return [card.get('text', '') for card in deck_data['deck'] if card.get('text')]
    
    def get_deck_summary(self, deck_name: str) -> str:
        """Get a formatted summary of deck composition"""
        analysis = self.analyze_deck_composition(deck_name)
        if not analysis:
            return f"Deck {deck_name} not found or empty"
        
        summary = f"Deck: {deck_name}\n"
        summary += f"Total Cards: {analysis['total_cards']}\n"
        summary += f"Card Types: {analysis['card_types']}\n"
        summary += f"Main Skills: {analysis['skills']}\n"
        summary += f"Mana Curve: {analysis['mana_curve']}\n"
        summary += f"Elements: {analysis['elements']}\n"
        summary += f"Ability Cost Types: {analysis['ability_cost_types']}\n"
        
        return summary
    
    def compare_decks(self, deck1_name: str, deck2_name: str) -> Dict[str, Any]:
        """Compare two decks to identify differences and similarities"""
        deck1_analysis = self.analyze_deck_composition(deck1_name)
        deck2_analysis = self.analyze_deck_composition(deck2_name)
        
        if not deck1_analysis or not deck2_analysis:
            return {"error": "One or both decks not found"}
        
        comparison = {
            'deck1': deck1_name,
            'deck2': deck2_name,
            'card_count_diff': deck1_analysis['total_cards'] - deck2_analysis['total_cards'],
            'common_skills': set(deck1_analysis['skills'].keys()) & set(deck2_analysis['skills'].keys()),
            'unique_skills_deck1': set(deck1_analysis['skills'].keys()) - set(deck2_analysis['skills'].keys()),
            'unique_skills_deck2': set(deck2_analysis['skills'].keys()) - set(deck1_analysis['skills'].keys()),
            'common_elements': set(deck1_analysis['elements'].keys()) & set(deck2_analysis['elements'].keys()),
            'deck1_focus': max(deck1_analysis['skills'].items(), key=lambda x: x[1])[0] if deck1_analysis['skills'] else 'None',
            'deck2_focus': max(deck2_analysis['skills'].items(), key=lambda x: x[1])[0] if deck2_analysis['skills'] else 'None',
        }
        
        return comparison
    
    def get_all_deck_names(self) -> List[str]:
        """Get all available deck names"""
        return list(self.decks.keys())