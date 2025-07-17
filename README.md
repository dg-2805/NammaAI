# NammaAI — Bangalore Smart City Concierge 🧠

**NammaAI** is an adaptive AI agent designed to assist both **tourists** and **new residents** in navigating Bangalore. Built using the **Agno framework**, it features robust persona detection, session tracking, and hybrid information retrieval using both static city guides and live web data.

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

### Source Blending Logic

1. Always query PDF
2. Trigger web if dynamic keyword present
3. Blend PDF (stable) + Web (dynamic)
4. If conflict, mention both

### Persona Detection Logic

```
Input → Rules → Gemini LLM → Explicit Commands → Memory Update
```

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
│   ├── web_search.py       # SerpAPI integration
│   ├── llm_wrapper.py      # Gemini interface
│   └── utils.py            # PDF processing
├── data/
│   ├── bangalore_guide.pdf
│   ├── bangalore_guide.txt
│   ├── sessions.json
│   └── vector_store/
├── conversations/
│   ├── tourist_session.txt
│   ├── resident_session.txt
│   └── persona_switch.txt
├── namma_agent.py          # Agno-powered entry
├── main.py                 # Stateless CLI
├── main_with_sessions.py   # Session token support
├── session_manager.py      # File-based persistence
├── requirements.txt
├── prompts.md              # Prompt logic
└── README.md               # This file
```

---

## 🏃‍♂️ Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

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

*"Day 1: Bangalore Palace + Lalbagh. Day 2: Commercial Street + brewery! *Namaskara* (Hello!)"*

**Resident**:

```
I'm moving to Bangalore for work
```

*"₹25-35K/month for 2BHK. Avoid cross-city commute. *Dhanyavadagalu* (Thanks!)"*

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
