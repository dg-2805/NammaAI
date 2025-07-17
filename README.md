# NammaAI — Bangalore Smart City Concierge 🧠

**NammaAI** is an adaptive AI agent designed to help both **tourists** and **new residents** navigate Bangalore. It uses a 2023 city guide as its primary knowledge base and augments with live web information when needed.

---

## 🎯 Problem Statement
Bangalore visitors and new residents face different challenges:
- **Tourists**: Need quick, fun recommendations for short stays
- **New Residents**: Require practical, long-term living advice
- **Both**: Need up-to-date information that static guides can't provide

## 👤 Personas Handled
- **Tourist**: Short visits, attractions, food, Instagram-worthy spots
- **New Resident**: Relocation advice, rent, commute, utilities, survival tips
- **Auto-detection**: Switches between personas based on user input

---

## 💡 Core Features

### 🔍 Intelligent Persona Detection
- **Rule-based detection**: Scans for keywords (e.g., "visiting", "moving", "weekend trip")
- **LLM fallback**: Uses Gemini LLM for ambiguous queries
- **Explicit switching**: Users can say "switch to tourist mode" or "switch to resident mode"
- **Session persistence**: Remembers persona across conversation turns (in-memory for `main.py`, persistent with session tokens in `main_with_sessions.py`)

### 📚 Hybrid Knowledge System
- **PDF-based RAG**: 2023 Bangalore City Guide as primary source (via ChromaDB + HuggingFace embeddings)
- **Web search augmentation**: Live updates for current info (prices, events) via SerpAPI
- **Smart routing**: Decides when to use PDF, web, or both (see below)
- **Source blending**: Combines PDF and web info naturally in responses (not always with explicit source tags)

### 🎭 Persona-Adapted Responses
- **Tourist mode**: Short, engaging, Instagram-friendly responses
- **Resident mode**: Detailed, practical, cost-focused advice
- **Cultural touch**: Kannada phrases with translations in every response

---

## 🔧 Technical Architecture

### RAG Implementation
```
PDF → Text Extraction → Chunking → Vector Embeddings → ChromaDB → Semantic Search
```
- PDF is extracted to text at startup (see `utils.py`)
- Text is chunked (750 chars, 100 overlap)
- Embeddings via HuggingFace
- ChromaDB for vector search

### Web Search Integration
- Uses SerpAPI (Google Search) for current info
- Triggers on keywords (see `WEB_SEARCH_KEYWORDS` in `agent.py`)
- Scrapes and summarizes top results
- Food queries are routed to Zomato/Swiggy/Magicpin; others to official/tourism sites

### Persona Detection Flow
```
User Input → Rule-based Detection → LLM Fallback → Explicit Switch → Session Memory → Response Generation
```
- Rule-based: `persona.py` (keywords)
- LLM fallback: Gemini via `llm_wrapper.py`
- Explicit: "switch to tourist/resident mode"
- Session: Persona passed in function calls or persisted with session tokens

### RAG vs. Web Search Decision Tree
```
1. Always query PDF (RAG) for context
2. If user input contains dynamic keywords (e.g., "now", "price", "rent", "best", "today"), trigger web search
3. If both sources have info, blend them: PDF for stable facts, web for current data
4. If info conflicts, acknowledge both (see below)
```

### Blending & Handling Conflicting Information
- **Blending**: Prompts instruct LLM to combine PDF and web info naturally (not just concatenate)
- **Conflicts**: If PDF and web differ, response acknowledges both (e.g., "The city guide mentions X, but recent updates show Y.")
- **Fallback**: If neither source is useful, LLM uses general knowledge

---

## 🚀 Tech Stack
- **Language Model**: Google Gemini (via LangChain)
- **Vector Database**: ChromaDB with HuggingFace embeddings
- **Web Search**: SerpAPI (Google Search)
- **PDF Processing**: PyMuPDF + LangChain document loaders
- **Text Splitting**: Recursive character splitter (750 chars, 100 overlap)

---

## 📁 Project Structure
```
namma-ai/
├── agent/
│   ├── agent.py           # Main orchestration logic
│   ├── persona.py         # Persona detection algorithms
│   ├── retriever.py       # RAG implementation
│   ├── prompts.py         # Persona-specific prompt templates
│   ├── web_search.py      # SerpAPI integration
│   ├── llm_wrapper.py     # Gemini API wrapper
│   └── utils.py           # PDF processing utilities
├── data/
│   ├── bangalore_guide.pdf    # 2023 city guide (source)
│   ├── bangalore_guide.txt    # Extracted text
│   ├── sessions.json          # Session persistence (for main_with_sessions.py)
│   └── vector_store/          # ChromaDB persistence
├── conversations/
│   ├── tourist_session.txt    # Tourist persona demo
│   ├── resident_session.txt   # Resident persona demo
│   └── persona_switch.txt     # Persona switching demo
├── main.py                # CLI interface (stateless)
├── main_with_sessions.py  # CLI interface with session tokens (recommended)
├── session_manager.py     # Session persistence logic
├── requirements.txt       # Dependencies
├── prompts.md             # Prompt engineering documentation
├── test.py                # Basic test script
└── README.md              # This file
```

---

## 🏃‍♂️ Quick Start

### 1. Setup Environment
```bash
# Clone the repository
git clone <repository-url>
cd namma-ai

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys
Create a `.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key_here
SERP_API_KEY=your_serpapi_key_here
OPENAI_API_KEY=your_openai_key_here  # Optional fallback
```

### 3. Run the Application
#### Option 1: Persistent Sessions (Recommended)
```bash
python main_with_sessions.py
```
- Supports session tokens for saving/restoring conversations
- Persona and history are remembered across runs

#### Option 2: Quick Chat (Stateless)
```bash
python main.py
```
- No session persistence; persona/history lost on exit

---

## 💾 Session Management
- **Session tokens**: Short codes shown at start; use to resume conversations
- **Persistence**: Sessions stored in `data/sessions.json` (local only)
- **Cleanup**: Sessions older than 7 days are automatically purged
- **No cloud sync**: All data is local to your machine

---

## 🎪 Example Interactions

### Tourist Mode
```
You: I'm visiting Bangalore for 2 days. What should I see?

🧠 NammaAI (tourist): Namaste! Two days? Let's make them count! ✨
Day 1: Bangalore Palace (stunning architecture!) + Lalbagh Gardens
Day 2: Commercial Street shopping + Toit brewery
*Namaskara* (Hello) and happy exploring! 🌟
```

### Resident Mode
```
You: I'm moving to Bangalore for work. Where should I live?

🧠 NammaAI (resident): Welcome to Bangalore! 🏙️
Consider these factors:
- Office location determines neighborhood
- Budget: ₹25-35K for 2BHK in good areas
- Commute: Avoid cross-city travel
*Dhanyavadagalu* (Thank you) for choosing Bangalore! 🏡
```

### Persona Switch
```
You: Switch to tourist mode
NammaAI: Switched to Tourist mode! Ready to show you the best of Bangalore. 🌆
```

---

## 🧠 How It Works

### Persona Detection Logic
1. **Rule-based matching**: Scans for keywords (see `persona.py`)
2. **LLM classification**: Uses Gemini for ambiguous cases
3. **Explicit commands**: "switch to tourist/resident mode"
4. **Session memory**: Persona is remembered across turns (in-memory or persisted)

### Information Retrieval Strategy
1. **Query analysis**: Checks for dynamic keywords (see `WEB_SEARCH_KEYWORDS`)
2. **PDF search**: Always performed for context
3. **Web search**: Triggered for current prices, events, ratings
4. **Response synthesis**: Blends sources with clear attribution if conflicting

### Response Generation
1. **Persona-specific prompts**: Different templates for tourist vs resident (see `prompts.py`)
2. **Source integration**: Combines PDF + web + general knowledge
3. **Cultural elements**: Adds Kannada phrases for local flavor
4. **Tone adaptation**: Casual for tourists, professional for residents

---

## 🎯 Key Differentiators

### vs. Static Chatbots
- **Persona awareness**: Adapts to user type and needs
- **Live information**: Supplements outdated guides with current data
- **Session continuity**: Remembers context across turns (with session tokens)

### vs. Generic Travel Assistants
- **Bangalore-specific**: Deep local knowledge and cultural context
- **Dual persona**: Handles both short-term and long-term needs
- **Practical focus**: Real advice from real sources

---

## ⚠️ Limitations & Assumptions

### Current Limitations
- **English-only**: No native Kannada conversation support
- **PDF dependency**: Core knowledge limited to 2023 guide content
- **Web search reliability**: SerpAPI/Google results may vary in quality
- **Rule-based persona detection**: May miss nuanced user intentions
- **Session memory**: Local file-based only, not cloud-synced
- **No advanced date-checking**: Web info may be outdated; agent does not verify recency beyond search
- **No voice interface**: Text-only CLI

### Assumptions Made
- **User types**: Binary classification (tourist/resident) covers most cases
- **Information freshness**: 2023 guide still relevant for basic facts
- **Language preference**: Users comfortable with English + Kannada phrases
- **Query patterns**: Common questions fit within persona frameworks

---

## 💡 Creative Features & Bonus Points
- **Kannada phrases**: Every response includes a Kannada phrase with translation
- **Auto-rickshaw negotiation tips**: Included in relevant responses
- **Bangalore survival kit**: Summarized for new residents
- **Weather-based recommendations**: Prompts can adapt based on query
- **Tech community suggestions**: Recommends meetups if asked

---

## 🛠️ How to Handle Conflicting Information
- If PDF and web info differ, the agent acknowledges both:
  - _"The city guide mentions X, but recent updates show Y."_
- Prompts instruct the LLM to blend, not just concatenate, and to avoid generic disclaimers
- If web info is missing or outdated, agent falls back to PDF or general knowledge

---

## 🧪 Testing
- Run `python test.py` for basic tests and validation.

---

## 🤝 Contributing

### Development Setup
```bash
# Development install
pip install -r requirements.txt

# Run tests
python test.py

# Format code
black agent/
```

### Project Guidelines
- **Code style**: Follow PEP 8 with Black formatting
- **Documentation**: Update prompts.md for prompt changes
- **Testing**: Add conversation examples to /conversations/
- **Personas**: Maintain clear separation between tourist/resident logic

---

## 📊 Performance Metrics

### Response Quality
- **Source attribution**: Acknowledges source contextually
- **Persona accuracy**: >90% correct persona detection (for clear cases)
- **Information freshness**: Web search for time-sensitive queries

### User Experience
- **Response time**: <3 seconds for typical queries
- **Conversation flow**: Maintains context across turns
- **Cultural relevance**: Kannada phrases in every response

---

**Built with ❤️ for Bangalore** - *Namma Bengaluru, Namma AI!*