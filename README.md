# LangChain for LLM Application Development - Certification Journey

## 🎯 Purpose

This repository documents my journey through the **[LangChain for LLM Application Development](https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/)** course by DeepLearning.AI, taught by Harrison Chase (LangChain Co-Founder/CEO) and Andrew Ng. The goal is to gain certification and build practical skills to become an **AI Engineer**.


### What You'll Learn
- Expand LLM capabilities using the LangChain framework
- Apply LLMs to proprietary data and build personal assistants
- Create specialized chatbots with memory and context
- Use agents, chained calls, and memories effectively
- Build production-ready LLM applications

## 🗂️ Repository Structure

```
langchain-certification/
├── README.md                    # This file
├── .env.example                # Template for API keys
├── lesson/                     # Course materials and notes
│   ├── L1-Model_prompt_parser.py  # Lesson 1: Models, Prompts and Parsers
│   ├── L2-Memory.py           # Lesson 2: Memory
│   └── README.md              # Lesson descriptions
├── projects/                   # Practical implementations
│   ├── lesson1_primal_tcg/   # Real-world application of Lesson 1
│   │   ├── primal_tcg_rules_assistant.py  # Main implementation
│   │   ├── test_primal_assistant.py       # Testing without API
│   │   ├── README_primal_tcg.md          # Project documentation
│   │   └── venv/                          # Virtual environment
│   └── lesson2_memory_trading/ # Real-world application of Lesson 2
│       └── README.md          # Project documentation
└── docs/                      # Additional documentation
    └── Primal_TCG_Comprehensive_Rules_V1.3.1.md
```

## 📖 Course Syllabus & Progress

### ✅ Lesson 1: Introduction (3 mins)
- Course overview and objectives

### ✅ Lesson 2: Models, Prompts and Parsers (18 mins)
- **Status:** Completed
- **Topics:** 
  - Direct API calls to OpenAI
  - Prompt templates with LangChain
  - Output parsers for structured data
- **Project:** [Primal TCG Rules Assistant](./projects/lesson1_primal_tcg/)
  - Built a rules clarification system for trading card game
  - Implemented structured output parsing for analytics
  - Created chained prompts for complex interactions

### ✅ Lesson 3: Memory (17 mins)
- **Status:** Completed
- **Topics:** 
  - ConversationBufferMemory for full history
  - ConversationSummaryMemory for condensed context
  - ConversationBufferWindowMemory for recent messages
  - Memory integration with chains
- **Project:** [Memory Trading Assistant](./projects/lesson2_memory_trading/)
  - Built a trading assistant with persistent memory
  - Implemented context-aware market analysis
  - Created conversational trading strategy discussions

### ⏳ Lesson 4: Chains (13 mins)
- **Status:** Upcoming
- **Topics:** Creating sequences of operations

### ⏳ Lesson 5: Question and Answer (15 mins)
- **Status:** Upcoming
- **Topics:** Applying LLMs to proprietary data

### ⏳ Lesson 6: Evaluation (15 mins)
- **Status:** Upcoming
- **Topics:** Testing and evaluating LLM applications

### ⏳ Lesson 7: Agents (14 mins)
- **Status:** Upcoming
- **Topics:** LLMs as reasoning agents

### ⏳ Lesson 8: Conclusion (1 min)
- **Status:** Upcoming
- **Topics:** Course wrap-up and next steps

## 🛠️ Technologies Used

- **Python 3.13+**
- **LangChain** - Core framework for LLM applications
- **OpenAI API** - Language model provider
- **langchain-openai** - OpenAI integration for LangChain
- **python-dotenv** - Environment variable management

## 🚀 Getting Started

### Prerequisites
1. Python 3.7+ installed
2. OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd langchain-certification

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install python-dotenv openai langchain langchain-openai langchain-community

# Set up environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Running Projects

Each lesson has its own project directory. For example:

```bash
# Navigate to a project
cd projects/lesson1_primal_tcg

# Activate virtual environment
source venv/bin/activate

# Run the project
python primal_tcg_rules_assistant.py
```

## 💡 Key Learning Outcomes

### From Lesson 1: Models, Prompts and Parsers
- ✅ Direct API calls vs LangChain abstractions
- ✅ Creating reusable prompt templates
- ✅ Parsing LLM outputs into structured JSON
- ✅ Building production-ready applications with error handling
- ✅ Implementing analytics and pattern tracking

### From Lesson 2: Memory
- ✅ Implementing conversation memory in applications
- ✅ Managing different memory types for optimal performance
- ✅ Building context-aware chatbots
- ✅ Persisting conversation history across sessions
- ✅ Memory optimization strategies for long conversations

## 🎓 Certification Goal

Upon completion of this course, I aim to:
1. **Gain DeepLearning.AI certification** in LangChain development
2. **Build a portfolio** of practical LLM applications
3. **Develop skills** required for AI Engineering roles
4. **Master LangChain** framework for production use

## 📈 Progress Tracking

- **Course Started:** August 2025
- **Lessons Completed:** 2/8
- **Projects Built:** 2
- **Lines of Code:** 800+
- **API Integrations:** OpenAI

## 🔗 Resources

- [Course Link](https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [DeepLearning.AI](https://www.deeplearning.ai/)

## 📝 Notes

This repository serves as both a learning journal and a practical implementation guide. Each project demonstrates real-world applications of the concepts learned, going beyond simple tutorials to create functional, production-ready systems.

## 🤝 Acknowledgments

- **Harrison Chase** - LangChain Co-Founder/CEO & Course Instructor
- **Andrew Ng** - DeepLearning.AI Founder & Course Instructor
- **DeepLearning.AI** - For providing this comprehensive course

---

*This repository is part of my journey to become an AI Engineer, focusing on practical applications of LLMs using the LangChain framework.*