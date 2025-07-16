# NammaAI — Bangalore Smart City Concierge 🧠

**NammaAI** is an adaptive AI agent designed to help both **tourists** and **new residents** navigate Bangalore. It uses a 2023 city guide as its knowledge base and augments with live web info.

## 👤 Personas Handled
- **Tourist**: Short visits, fun places, food, transport
- **New Resident**: Long-term relocation, practical advice (rent, commute, ISPs)

## 💡 Features
- PDF-based semantic search (via LangChain + Chroma)
- Persona detection via keyword heuristics (extendable to LLM)
- Live web integration for fresh info (DuckDuckGo API)
- Persona-adapted prompt engineering
- Stateful memory (persona remembered across turns)

## 🔍 Flow
1. User asks a question
2. Persona detected
3. PDF vector store searched
4. Web search triggered if info might be outdated
5. Response generated with persona-specific prompt

## 🚀 Tech Stack
- Python + LangChain + OpenAI + DuckDuckGo
- FAISS/Chroma for vector storage
- CLI interface via `main.py`

## 📁 Folder Structure
```
/agent
  agent.py
  persona.py
  retriever.py
  prompts.py
  web_search.py
/data
  bangalore_guide.pdf
  vector_store/
/conversations
  tourist_session.txt
  resident_session.txt
  persona_switch.txt
README.md
prompts.md
main.py
```

## ✅ How to Run
1. Add your OpenAI key in `.env`:
   ```
   OPENAI_API_KEY="sk-..."
   ```
2. Run:
   ```bash
   pip install -r requirements.txt
   python main.py
   ```

## ⚠️ Assumptions & Notes
- Persona detection is rule-based (accurate for obvious cues)
- Web results not always guaranteed fresh — fallback included
- PDF is outdated by nature — search used sparingly