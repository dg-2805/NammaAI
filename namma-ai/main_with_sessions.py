"""
NammaAI Main Application with Session Management

Purpose: Enhanced version of main.py that includes session token functionality.
Allows users to save and restore conversation sessions with persona and history persistence.

Features:
- Session token generation for conversation persistence
- Persona and conversation history restoration
- Enhanced user experience with session management
- Compatible with the core NammaAI agent system

Usage: python main_with_sessions.py
"""

from agent.agent import generate_response
from session_manager import SessionManager

def chat():
    session_manager = SessionManager()
    
    print("👋 Welcome to NammaAI — Your Bangalore Smart City Concierge!")
    print("🔄 Do you have a session token? (Enter token or press Enter for new session)")
    
    session_token = input("Session Token: ").strip()
    
    if session_token:
        session_data = session_manager.get_session(session_token)
        if session_data:
            print(f"✅ Welcome back! Session restored.")
            session_persona = session_data.get("persona")
            conversation_history = session_data.get("conversation_history", [])
        else:
            print("❌ Invalid session token. Creating new session.")
            session_token = session_manager.create_session()
            session_persona = None
            conversation_history = []
    else:
        session_token = session_manager.create_session()
        session_persona = None
        conversation_history = []
    
    print(f"📱 Your session token: {session_token}")
    print("💡 Save this token to resume your session later!")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! 👋")
            print(f"💾 Your session token: {session_token}")
            break

        response, detected = generate_response(user_input, session_persona, conversation_history)
        
        # Add to conversation history
        conversation_history.append(f"User: {user_input}")
        conversation_history.append(f"AI: {response}")
        
        # Keep only last 6 exchanges (3 user + 3 AI responses) to avoid context overflow
        if len(conversation_history) > 6:
            conversation_history = conversation_history[-6:]
        
        # Only update session_persona if a new, non-unknown persona is detected
        if detected != "unknown" and detected != session_persona:
            session_persona = detected

        # Update session after each interaction
        session_manager.update_session(
            session_token, 
            persona=session_persona,
            conversation_history=conversation_history
        )

        print(f"\n🧠 NammaAI ({session_persona or detected}): {response}")

if __name__ == "__main__":
    chat()
