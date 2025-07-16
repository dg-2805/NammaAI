from agent.agent import generate_response

def chat():
    print("👋 Welcome to NammaAI — Your Bangalore Smart City Concierge!")
    session_persona = None
    conversation_history = []

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! 👋")
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

        print(f"\n🧠 NammaAI ({session_persona or detected}): {response}")

if __name__ == "__main__":
    chat()
