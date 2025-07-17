# NammaAI — Bangalore Smart City Concierge 🧠

**NammaAI** is an adaptive AI agent designed to assist both **tourists** and **new residents** in navigating Bangalore. Built using the **Agno framework**, it features robust persona detection, session tracking, and hybrid information retrieval using both static city guides and live web data.

---
> ⚠️ **Developer Note**
>
> - For best results, use **`main.py`** or **`main_with_sessions.py`**. These are the most stable and well-structured versions of the agent logic.
> - `namma_agent.py` was a **last-minute AGNO integration** and may not reflect clean architecture.
> - `main_weather.py` adds real-time weather support (OpenWeatherMap API) and is kept separate as a **bonus feature** to preserve the core logic.

---

## 🎯 Problem Statement

Bangalore visitors and new residents face different challenges:

* **Tourists**: Need quick, fun recommendations for short stays  
* **New Residents**: Require practical, long-term living advice  
* **Both**: Need up-to-date, reliable information

---

## 👤 Personas Handled

* **Tourist**: Short visits, attractions, food, Instagram-friendly spots  
* **New Resident**: Relocation advice, rent, commute, utilities  
* **Auto-detection**: Switches personas based on input

---

## 💡 Core Features

### 🤖 Agno Framework Integration

* Built on Agno's `Agent` class  
* Enhanced context & session analytics  
* Persistent conversation memory  

### 🔍 Intelligent Persona Detection

* Rule-based keywords (`persona.py`)  
* LLM fallback via Gemini (`llm_wrapper.py`)  
* Explicit commands ("switch to tourist mode")  
* Session memory using Agno context  

### 📚 Hybrid Knowledge System

* **PDF-based RAG**: 2023 Bangalore City Guide  
* **Web search augmentation** via SerpAPI  
* Smart routing between PDF/Web  
* Conflict handling & source attribution  

### 🎝️ Persona-Adapted Responses

* Tourist: Concise, fun, Insta-ready  
* Resident: Practical, detailed, cost-aware  
* Kannada phrases with translations  

---

## 🔧 Technical Architecture

### Agno Agent Flow

```

User Input → Agno Agent → Persona Detection → Context Management → Response Generation → Session Tracking

```

### Retrieval Augmented Generation (RAG)

```

PDF → Text → Chunking (750c, 100o) → HuggingFace Embeddings → ChromaDB → Semantic Search

```

### Web Search

* Triggers on dynamic keywords ("price", "today")  
* SerpAPI for scraping + summarizing  
* Food queries routed to Zomato, Swiggy, etc.

---

## 🧠 Behind the Scenes: Decision Making

### 👤 Persona Detection

```

User Input → Rules (persona.py) → Gemini fallback → Explicit command → Agno session memory

```

- **Rule-based detection**: Uses keyword heuristics (e.g., "I'm visiting" → Tourist).  
- **LLM fallback**: If rules are inconclusive, Gemini classifies the input contextually.  
- **Explicit switching**: Commands like `"switch to resident mode"` override all detection.  
- **Session memory**: Persona is stored in Agno's context and reused across turns.

---

### 🔍 RAG vs Web Search Decision Tree

```

Always query PDF
↓
If dynamic keywords detected (e.g., "today", "price", "weather") → Trigger web search
↓
Gemini blends PDF + Web content for answer generation
↓
If conflict → Mention both sources with attribution
↓
If LLM unavailable → Use PDF fallback only

```

- The **PDF guide** is the default, trusted source for stable, local knowledge.  
- **Web search** is only triggered for time-sensitive or real-time queries.  
- Gemini blends both sources to ensure reliable yet up-to-date responses.

---

### ⚖️ Conflict Resolution Strategy

When PDF and web info differ:

- **PDF takes priority** if the information is long-term or factual (e.g., transport zones, area names).  
- **Web data is prioritized** for time-sensitive topics (e.g., rent trends, weather, events).  
- If conflicting, both sources are shown with attribution. For example:

  > "According to the city guide, rent in Koramangala averages ₹25K.  
  > However, current listings suggest it may spike to ₹30K this month."

- Gemini flags possible inconsistencies and tries to preserve user trust with clarity.

---

## 🚀 Tech Stack

* **Agno Agent Framework**  
* **Google Gemini (via LangChain)**  
* **ChromaDB** (Vector Store)  
* **HuggingFace Embeddings**  
* **SerpAPI** (Live web)  
* **PyMuPDF** for PDF parsing  

---

## 📁 Project Structure

```

namma-ai/
├── agent/
│   ├── agent.py            # Orchestrates logic
│   ├── persona.py          # Rule-based detection
│   ├── retriever.py        # RAG implementation
│   ├── prompts.py          # Templates
│   ├── web\_search.py       # SerpAPI integration
│   ├── llm\_wrapper.py      # Gemini interface
│   └── utils.py            # PDF processing
├── data/
│   ├── bangalore\_guide.pdf
│   ├── bangalore\_guide.txt
│   ├── sessions.json
│   └── vector\_store/
├── conversations/
│   ├── tourist\_session.txt
│   ├── resident\_session.txt
│   └── persona\_switch.txt
├── namma\_agent.py          # Agno-powered entry
├── main.py                 # Stateless CLI
├── main\_with\_sessions.py   # Session token support
├── session\_manager.py      # File-based persistence
├── requirements.txt
├── prompts.md              # Prompt logic
└── README.md               # This file

````

---

## 🏃‍♂️ Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
````

### 2. Add API Keys in `.env`

```env
GEMINI_API_KEY=your_key
SERP_API_KEY=your_key
```

### 3. Run

```bash
python namma_agent.py  # RECOMMENDED
python main_with_sessions.py  # With session tokens
python main.py  # Stateless demo
```

---

## 🤖 Agno CLI Commands

* `session info`: View analytics
* `switch to tourist mode`: Change persona
* Exit auto-generates summary report

---

## 💮 Example Prompts

**Tourist**:

```
I'm visiting Bangalore for 2 days
```

*"Day 1: Bangalore Palace + Lalbagh. Day 2: Commercial Street + brewery! *Namaskara* (Hello!)*"

**Resident**:

```
I'm moving to Bangalore for work
```

*"₹25-35K/month for 2BHK. Avoid cross-city commute. *Dhanyavadagalu* (Thanks!)*"

**Switching**:

```
switch to tourist mode
```

---

## 🥇 Differentiators

* **Bangalore-specific**
* **Adaptive personas**
* **LLM + rules + explicit switching**
* **Smart source blending (PDF + Web)**
* **Session memory and analytics**

---

## ⚠️ Limitations

* No voice input
* PDF (2023) may get outdated
* Web info quality varies
* Local file-based memory only

---

## 🧪 Assignment Goals Met

* ✅ Agno integration
* ✅ Persona detection (rule + LLM + explicit)
* ✅ Hybrid retrieval (PDF + Web)
* ✅ Custom prompts + cultural embedding
* ✅ CLI + session management

---

**Built with ❤️ for Namma Bengaluru.**
*Namma Bengaluru. Namma AI!*

---

## Features

* Persona-aware answers for tourists and residents
* PDF (city guide) as primary knowledge source, web search as supplement
* Real-time weather integration (see below)
* Kannada phrases in all responses (including fallback)
* "Bangalore Survival Kit" and other special tips
* Robust fallback logic if LLM is unavailable

---

## Usage

### Standard CLI

```bash
python main.py
```

### CLI with Real-Time Weather

```bash
python main_weather.py
```

#### Weather API Setup

* Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
* Set your API key in your environment:

**Linux/macOS:**

```bash
export OPENWEATHER_API_KEY=your_api_key_here
```

**Windows CMD:**

```cmd
set OPENWEATHER_API_KEY=your_api_key_here
```

**Windows PowerShell:**

```powershell
$env:OPENWEATHER_API_KEY="your_api_key_here"
```

* The agent will automatically blend real-time weather info into answers if your query is about weather, rain, temperature, etc.

---

### Special Features

* **Kannada phrases:** Every answer (including fallback) ends with a Kannada phrase and translation.
* **Bangalore Survival Kit:** Ask for "survival kit" to get a summary of essential tips for new arrivals.
* **Fallbacks:** If the LLM (Gemini) is unavailable, you get a concise, relevant extract from the city guide, not a generic error.
* **Web search:** For current/dynamic info, web search is triggered and blended with PDF info by the LLM.

---

### Example Queries

* "Tell me about Lalbagh Botanical Garden"
* "How to negotiate with auto rickshaw drivers?"
* "What's the weather in Bangalore today?"
* "Give me a Bangalore survival kit"
* "Any tech meetups in Bangalore this week?"

---

## Developer Notes

* All entry points use the same core agent logic for consistency.
* To add more special commands, see the start of `generate_response` in `agent/agent.py`.
* For fallback logic, see the end of `generate_response` in `agent/agent.py`.

---

For more details, see the code and comments in the `namma-ai/` directory.
