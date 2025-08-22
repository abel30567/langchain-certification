# Lesson 4 Project: Primal TCG Q&A System

A comprehensive Question & Answer system for Primal TCG using RetrievalQA, vector stores, and multiple retrieval strategies. Demonstrates concepts from Lesson 4: Q&A over Documents.

## 🎯 Project Overview

This project implements an advanced Q&A system that can:
- Answer deck building questions with specific card recommendations
- Search and filter cards based on various attributes
- Clarify game rules with precise citations
- Compare cards and strategies
- Maintain conversational context for iterative deck building

## 🏗️ Architecture

### Document Processing Strategy

**Design Decision**: Mixed approach optimized for different data types

1. **Cards (CSV)** → Individual documents with rich metadata
   - Rationale: Enable precise filtering and card-specific searches
   - Each card becomes a searchable document with structured metadata

2. **Rules (Markdown)** → Chunked with overlap
   - Rationale: Preserve context while keeping chunks manageable
   - Uses MarkdownTextSplitter to maintain structure

3. **Decks (JSON)** → Overview + Details documents
   - Rationale: Support both high-level analysis and specific card queries
   - Creates composition overview and detailed card lists

### Retrieval Strategies

1. **Similarity Search** - Standard cosine similarity
2. **MMR (Maximum Marginal Relevance)** - Balances relevance with diversity
3. **Threshold Search** - Only returns high-confidence matches
4. **Hybrid Search** - Combines results from cards, rules, and decks

### QA Chain Types

1. **Deck Building Chain** - Optimized for synergy and strategy questions
2. **Card Search Chain** - Formats results as markdown tables
3. **Rules Chain** - Provides precise rulings with citations
4. **Comparison Chain** - Structured comparisons with pros/cons
5. **Conversational Chain** - Maintains memory across queries

## 📁 Project Structure

```
lesson4_qna_primal/
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── data/                      # Data sources
│   ├── cards.csv             # Card database
│   ├── rules.md              # Comprehensive rules
│   ├── deck1.json            # Sample deck 1
│   ├── deck2.json            # Sample deck 2
│   └── deck3.json            # Sample deck 3
├── loaders/
│   ├── __init__.py
│   └── document_loader.py    # Multi-source document loading
├── retrievers/
│   ├── __init__.py
│   └── vector_store.py       # Vector store with multiple strategies
├── chains/
│   ├── __init__.py
│   └── qa_chain.py           # RetrievalQA implementations
├── utils/
│   ├── __init__.py
│   └── formatters.py         # Response formatting utilities
├── demo_interactive.py        # Interactive demonstration
└── demo_automatic.py         # Automatic showcase
```

## 🚀 Getting Started

### Installation

1. Navigate to project directory:
```bash
cd projects/lesson4_qna_primal
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment:
```bash
echo "OPENAI_API_KEY=your_key_here" > .env
```

## 🎮 Running the Demos

### Interactive Demo
```bash
python demo_interactive.py
```

**Features:**
- 8 different modes including deck building, card search, rules
- Query type selection or auto-detection
- Conversational mode with memory
- Retrieval strategy testing

### Automatic Demo
```bash
python demo_automatic.py
```

**Demonstrates:**
1. Basic document retrieval
2. Different QA chain types
3. Advanced retrieval strategies
4. Conversational Q&A with memory
5. Document processing decisions
6. Comprehensive deck building query
7. Performance comparison

## 💡 Key Features

### Advanced Retrieval
- **Similarity Search**: Find most relevant documents
- **MMR Search**: Get diverse results for varied perspectives
- **Hybrid Search**: Combine cards, rules, and deck information
- **Smart Retriever**: Auto-selects best strategy based on query

### Specialized Chains
Each chain type has custom prompts optimized for its purpose:
- Deck building focuses on synergies and competitive viability
- Card search formats results as tables
- Rules provides precise citations
- Comparison creates structured analyses

### Document Processing Innovation
```python
# Decision: Keep cards as individual documents
# Rationale: Enable metadata filtering
enhanced_doc = Document(
    page_content=enhanced_content,  # Searchable text
    metadata={
        'doc_type': 'card',
        'elements': ['Fire', 'Air'],
        'total_cost': 3,
        'rarity': 'Legendary'
    }
)
```

## 📊 Example Queries

### Deck Building
- "What cards work well with Synthetic Laboratory?"
- "Build a Fire/Air aggro deck"
- "Suggest TRIGGER ability synergies"

### Card Search
- "Show all Fire cards under 3 cost"
- "List cards with REBIRTH"
- "Find Synthetic Life creatures"

### Rules
- "How does TRIGGER stacking work?"
- "Explain combat phases"
- "When can I activate abilities?"

### Comparison
- "Compare Fire vs Air for aggro"
- "TRIGGER vs ACTIVATE abilities"
- "Which attribute is better: BIO or PLEAGUIS?"

## 🔍 Retrieval Strategy Comparison

| Strategy | Best For | Pros | Cons |
|----------|----------|------|------|
| Similarity | Specific queries | Fast, accurate | May lack diversity |
| MMR | Deck building | Diverse results | Slightly slower |
| Hybrid | General queries | Comprehensive | More complex |
| Threshold | High-precision needs | Only confident matches | May miss relevant docs |

## 📈 Performance Optimizations

1. **Smart Chunking**: Different strategies per document type
2. **Metadata Filtering**: Reduces search space
3. **Query Routing**: Automatic chain selection
4. **Caching**: Vector store persists embeddings
5. **Batch Processing**: Load all documents efficiently

## 🎯 Learning Outcomes

This project demonstrates:
1. **Document Loading**: Multiple file formats (CSV, MD, JSON)
2. **Text Splitting**: Strategic chunking for different content types
3. **Embeddings**: OpenAI embeddings for semantic search
4. **Vector Stores**: Both in-memory and persistent options
5. **RetrievalQA**: Multiple chain types with custom prompts
6. **Advanced Retrieval**: MMR, threshold, and hybrid strategies
7. **Conversational Memory**: Multi-turn interactions

## 🔧 Customization

### Add New Data Sources
1. Place files in `data/` directory
2. Extend `PrimalTCGDocumentLoader` class
3. Define processing strategy

### Create Custom Chains
1. Add new prompt template in `qa_chain.py`
2. Register chain type in `_initialize_chains()`
3. Update query type detection

### Modify Retrieval
1. Adjust search parameters in `vector_store.py`
2. Change embedding model if needed
3. Switch between Chroma/in-memory storage

## 📝 Key Innovations

1. **Multi-Source Integration**: Seamlessly combines cards, rules, and decks
2. **Smart Query Routing**: Automatically selects best chain type
3. **Metadata-Rich Documents**: Enables precise filtering
4. **Conversational Deck Building**: Iterative refinement with memory
5. **Format-Aware Responses**: Tables for cards, structured text for rules

## 🤝 Acknowledgments

- Built for LangChain for LLM Application Development course
- Uses Primal TCG game system
- Demonstrates Lesson 4: Q&A over Documents concepts

---

*This project showcases advanced RetrievalQA techniques applied to a real trading card game, demonstrating how to build production-ready Q&A systems with LangChain.*