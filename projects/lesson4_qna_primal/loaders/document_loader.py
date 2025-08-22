"""
Document Loader for Primal TCG Q&A System
Loads and processes cards CSV, rules markdown, and deck JSON files
"""

import json
import os
from typing import List, Dict, Any
from langchain_community.document_loaders import TextLoader, DataFrameLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownTextSplitter
import pandas as pd


class PrimalTCGDocumentLoader:
    """
    Comprehensive document loader for all Primal TCG data sources.
    
    Design Decision: Mixed approach for document processing
    - Cards: Keep as individual documents with rich metadata for filtering
    - Rules: Split into chunks for granular retrieval
    - Decks: Convert to structured documents with composition analysis
    
    This approach balances search granularity with context preservation.
    """
    
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.data_dir = os.path.join(current_dir, "data")
        else:
            self.data_dir = data_dir
            
        self.documents = []
        self.cards_docs = []
        self.rules_docs = []
        self.deck_docs = []
        
    def load_all_documents(self) -> List[Document]:
        """Load all document types and return combined list"""
        self.load_cards()
        self.load_rules()
        self.load_decks()
        
        # Combine all documents
        self.documents = self.cards_docs + self.rules_docs + self.deck_docs
        return self.documents
    
    def load_cards(self) -> List[Document]:
        """
        Load cards from CSV with enhanced metadata.
        Each card becomes a single document with structured metadata for filtering.
        """
        csv_path = os.path.join(self.data_dir, "cards.csv")
        
        if not os.path.exists(csv_path):
            print(f"Warning: Cards CSV not found at {csv_path}")
            return []
        
        # Read CSV with pandas (supports multi-char delimiter)
        df = pd.read_csv(csv_path, sep='\\|\\|', engine='python')
        
        # Limit to first 50 cards for demo purposes to avoid token limits
        df = df.head(50)
        
        # Convert DataFrame rows to documents
        for _, row in df.iterrows():
            # Create content string from row data
            content_lines = []
            for col in df.columns:
                if pd.notna(row[col]):
                    content_lines.append(f"{col}: {row[col]}")
            content = '\n'.join(content_lines)
            
            # Create enhanced content with searchable format
            enhanced_content = self._enhance_card_content(content)
            
            # Extract metadata for filtering
            metadata = self._extract_card_metadata(content)
            metadata['source'] = 'card'
            metadata['doc_type'] = 'card'
            
            # Create new document with enhanced content and metadata
            enhanced_doc = Document(
                page_content=enhanced_content,
                metadata=metadata
            )
            self.cards_docs.append(enhanced_doc)
        
        print(f"Loaded {len(self.cards_docs)} card documents")
        return self.cards_docs
    
    def load_rules(self) -> List[Document]:
        """
        Load and split rules document for granular retrieval.
        Uses MarkdownTextSplitter to preserve structure.
        """
        rules_path = os.path.join(self.data_dir, "rules.md")
        
        if not os.path.exists(rules_path):
            print(f"Warning: Rules document not found at {rules_path}")
            return []
        
        # Load the markdown file
        with open(rules_path, 'r', encoding='utf-8') as f:
            rules_text = f.read()
        
        # Split by sections for better context
        splitter = MarkdownTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            length_function=len
        )
        
        # Create documents from splits
        splits = splitter.split_text(rules_text)
        
        # Limit to first 100 chunks for demo purposes
        splits = splits[:100]
        
        for i, split in enumerate(splits):
            doc = Document(
                page_content=split,
                metadata={
                    'source': 'rules',
                    'doc_type': 'rules',
                    'section_index': i,
                    'total_sections': len(splits)
                }
            )
            self.rules_docs.append(doc)
        
        print(f"Loaded {len(self.rules_docs)} rules document chunks")
        return self.rules_docs
    
    def load_decks(self) -> List[Document]:
        """
        Load deck JSON files and convert to searchable documents.
        Creates both overview and detailed card list documents.
        """
        deck_files = [f for f in os.listdir(self.data_dir) if f.endswith('.json')]
        
        for deck_file in deck_files:
            deck_path = os.path.join(self.data_dir, deck_file)
            deck_name = deck_file.replace('.json', '')
            
            with open(deck_path, 'r', encoding='utf-8') as f:
                deck_data = json.load(f)
            
            # Create deck overview document
            overview_doc = self._create_deck_overview(deck_data, deck_name)
            if overview_doc:
                self.deck_docs.append(overview_doc)
            
            # Create detailed card list document
            detail_doc = self._create_deck_details(deck_data, deck_name)
            if detail_doc:
                self.deck_docs.append(detail_doc)
        
        print(f"Loaded {len(self.deck_docs)} deck documents")
        return self.deck_docs
    
    def _enhance_card_content(self, content: str) -> str:
        """
        Enhance card content for better retrieval.
        Formats the content in a more searchable way.
        """
        lines = content.split('\n')
        card_dict = {}
        
        for line in lines:
            if ': ' in line:
                key, value = line.split(': ', 1)
                card_dict[key.strip()] = value.strip()
        
        # Create enhanced searchable content
        enhanced = []
        
        # Name and type first
        if 'Name' in card_dict:
            enhanced.append(f"Card Name: {card_dict['Name']}")
        if 'Card Type' in card_dict:
            enhanced.append(f"Type: {card_dict['Card Type']}")
        
        # Key attributes
        if 'Elements' in card_dict:
            enhanced.append(f"Elements: {card_dict['Elements']}")
        if 'Cost' in card_dict:
            enhanced.append(f"Cost: {card_dict['Cost']}")
        if 'Attribute' in card_dict:
            enhanced.append(f"Attribute/Skill: {card_dict['Attribute']}")
        
        # Effect (most important for deck building)
        if 'Effect' in card_dict:
            enhanced.append(f"Effect: {card_dict['Effect']}")
        
        # Stats for characters
        if 'Healthy' in card_dict:
            enhanced.append(f"Stats (Healthy): {card_dict['Healthy']}")
        if 'Injured' in card_dict:
            enhanced.append(f"Stats (Injured): {card_dict['Injured']}")
        
        # Additional info
        if 'Rarity' in card_dict:
            enhanced.append(f"Rarity: {card_dict['Rarity']}")
        if 'Card Set' in card_dict:
            enhanced.append(f"Set: {card_dict['Card Set']}")
        
        return '\n'.join(enhanced)
    
    def _extract_card_metadata(self, content: str) -> Dict[str, Any]:
        """Extract structured metadata from card content for filtering"""
        lines = content.split('\n')
        metadata = {}
        
        for line in lines:
            if ': ' in line:
                key, value = line.split(': ', 1)
                key = key.strip().lower().replace(' ', '_')
                metadata[key] = value.strip()
        
        # Extract specific attributes for filtering
        if 'elements' in metadata:
            elements = metadata['elements'].split()
            metadata['element_list'] = elements
            metadata['element_count'] = len(elements)
        
        if 'cost' in metadata and metadata['cost']:
            # Parse cost for filtering (e.g., "2 F F" means 2 colorless + 2 fire)
            cost_parts = metadata['cost'].split()
            total_cost = 0
            for part in cost_parts:
                if part.isdigit():
                    total_cost += int(part)
                else:
                    total_cost += 1  # Each letter represents 1 mana
            metadata['total_cost'] = total_cost
        
        if 'turn_count' in metadata:
            try:
                metadata['turn_count_int'] = int(metadata['turn_count'])
            except:
                metadata['turn_count_int'] = 0
        
        return metadata
    
    def _create_deck_overview(self, deck_data: Dict, deck_name: str) -> Document:
        """Create an overview document for a deck"""
        if 'deck' not in deck_data:
            return None
        
        deck_cards = deck_data['deck']
        
        # Analyze deck composition
        card_types = {}
        elements = {}
        skills = {}
        total_cards = len(deck_cards)
        
        for card in deck_cards:
            # Count card types
            card_type = card.get('cardType', 'Unknown')
            card_types[card_type] = card_types.get(card_type, 0) + 1
            
            # Count elements
            if 'element' in card and card['element']:
                for elem in card['element']:
                    elements[elem] = elements.get(elem, 0) + 1
            
            # Count skills/attributes
            skill = card.get('skill', '')
            if skill:
                skills[skill] = skills.get(skill, 0) + 1
        
        # Create overview content
        content = f"""Deck: {deck_name}
Total Cards: {total_cards}

Card Type Distribution:
{self._format_distribution(card_types)}

Element Distribution:
{self._format_distribution(elements)}

Skill/Attribute Distribution:
{self._format_distribution(skills)}

This deck focuses on {', '.join(list(skills.keys())[:3])} strategies with {', '.join(list(elements.keys())[:2])} elements.
"""
        
        return Document(
            page_content=content,
            metadata={
                'source': 'deck',
                'doc_type': 'deck_overview',
                'deck_name': deck_name,
                'total_cards': total_cards,
                'main_elements': list(elements.keys())[:2],
                'main_skills': list(skills.keys())[:3]
            }
        )
    
    def _create_deck_details(self, deck_data: Dict, deck_name: str) -> Document:
        """Create a detailed card list document for a deck"""
        if 'deck' not in deck_data:
            return None
        
        deck_cards = deck_data['deck']
        
        # Group cards by type for better organization
        characters = []
        abilities = []
        fields = []
        strategies = []
        
        for card in deck_cards:
            card_info = f"- {card.get('name', 'Unknown')}: {card.get('text', 'No effect')[:100]}..."
            
            card_type = card.get('cardType', '').lower()
            if 'character' in card_type:
                characters.append(card_info)
            elif 'ability' in card_type:
                abilities.append(card_info)
            elif 'field' in card_type:
                fields.append(card_info)
            elif 'strategy' in card_type:
                strategies.append(card_info)
        
        content = f"""Deck Card List: {deck_name}

Characters ({len(characters)}):
{chr(10).join(characters[:20])}  # Limit to first 20 for space

Abilities ({len(abilities)}):
{chr(10).join(abilities[:10])}

Fields ({len(fields)}):
{chr(10).join(fields[:5])}

Strategies ({len(strategies)}):
{chr(10).join(strategies[:5])}
"""
        
        return Document(
            page_content=content,
            metadata={
                'source': 'deck',
                'doc_type': 'deck_details',
                'deck_name': deck_name,
                'character_count': len(characters),
                'ability_count': len(abilities)
            }
        )
    
    def _format_distribution(self, dist: Dict) -> str:
        """Format a distribution dictionary as a readable string"""
        sorted_items = sorted(dist.items(), key=lambda x: x[1], reverse=True)
        return '\n'.join([f"  - {key}: {value}" for key, value in sorted_items[:10]])  # Top 10