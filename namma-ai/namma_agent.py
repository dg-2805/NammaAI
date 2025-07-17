"""
NammaAI Agent - Agno-powered Bangalore Smart City Concierge

This module implements the main NammaAI agent using the Agno framework
while leveraging existing persona detection and response generation logic.
"""

from agno.agent import Agent
from agent.agent import generate_response, detect_persona, llm_detect_persona, explicit_persona_switch
import json

class NammaAIAgent(Agent):
    """
    Agno-powered NammaAI agent that combines framework capabilities
    with custom Bangalore-specific logic for persona detection and responses.
    """
    
    def __init__(self):
        super().__init__()
        self.persona_detection_enabled = True
        self.conversation_memory = {}
        
    def detect_user_persona(self, message: str, context: dict) -> str:
        """
        Enhanced persona detection using both existing logic and agno capabilities.
        
        Args:
            message: User's input message
            context: Session context with history
            
        Returns:
            Detected persona: 'tourist', 'resident', 'ambiguous', or 'unknown'
        """
        try:
            # First, check for explicit persona switching
            explicit_switch = explicit_persona_switch(message)
            if explicit_switch:
                return explicit_switch
                
            # Use existing rule-based detection
            detected_persona = detect_persona(message)
            
            # If unknown, fall back to LLM detection
            if detected_persona == "unknown":
                detected_persona = llm_detect_persona(message)
                
            # Store detection result in agno context for tracking
            context['last_persona_detection'] = {
                'message': message,
                'detected': detected_persona,
                'method': 'rule-based' if detected_persona != 'unknown' else 'llm-fallback'
            }
            
            return detected_persona
            
        except Exception as e:
            print(f"Error in persona detection: {e}")
            return "unknown"

    def on_message(self, message: str, context: dict) -> str:
        """
        Main message handler that processes user input through agno framework
        while using existing NammaAI logic.
        
        Args:
            message: User's input message
            context: Agno session context
            
        Returns:
            Generated response from NammaAI system
        """
        try:
            # Initialize context if new session
            if not context.get('initialized'):
                context['initialized'] = True
                context['conversation_history'] = []
                context['persona'] = None
                context['session_stats'] = {
                    'total_messages': 0,
                    'persona_switches': 0,
                    'web_searches_triggered': 0
                }
            
            # Update session statistics
            context['session_stats']['total_messages'] += 1
            
            # Enhanced persona detection using agno + existing logic
            session_persona = context.get('persona')
            detected_persona = self.detect_user_persona(message, context)
            
            # Track persona switches
            if detected_persona != "unknown" and detected_persona != session_persona:
                context['session_stats']['persona_switches'] += 1
                session_persona = detected_persona
                context['persona'] = session_persona
                
            # Get conversation history
            conversation_history = context.get('conversation_history', [])
            
            # Generate response using existing NammaAI logic
            response, final_persona = generate_response(
                message, 
                session_persona, 
                conversation_history
            )
            
            # Update conversation history
            conversation_history.append(f"User: {message}")
            conversation_history.append(f"AI: {response}")
            
            # Keep only last 6 exchanges to manage context size
            if len(conversation_history) > 6:
                conversation_history = conversation_history[-6:]
                
            context['conversation_history'] = conversation_history
            
            # Update persona if it changed during response generation
            if final_persona != session_persona and final_persona != "unknown":
                context['persona'] = final_persona
                
            # Store enhanced response metadata in agno context
            context['last_response_metadata'] = {
                'persona_used': final_persona,
                'message_length': len(response),
                'conversation_turn': len(conversation_history) // 2
            }
            
            return response
            
        except Exception as e:
            print(f"Error in on_message: {e}")
            return "I apologize, but I encountered an error processing your message. Please try again."
    
    def get_session_summary(self, context: dict) -> dict:
        """
        Agno-enhanced session summary with detailed analytics.
        
        Args:
            context: Current session context
            
        Returns:
            Comprehensive session summary
        """
        stats = context.get('session_stats', {})
        return {
            'current_persona': context.get('persona', 'unknown'),
            'total_interactions': stats.get('total_messages', 0),
            'persona_switches': stats.get('persona_switches', 0),
            'conversation_length': len(context.get('conversation_history', [])),
            'last_detection_method': context.get('last_persona_detection', {}).get('method', 'none'),
            'session_initialized': context.get('initialized', False)
        }

def run_cli():
    """
    Enhanced CLI interface with agno integration and automatic persona detection.
    """
    agent = NammaAIAgent()
    context = {}
    
    print("🧠 NammaAI - Bangalore Smart City Concierge (Powered by Agno)")
    print("=" * 60)
    print("👋 Welcome! I can help you as a tourist or new resident.")
    print("💡 Try: 'I'm visiting for the weekend' or 'I'm moving here for work'")
    print("Type 'session info' for session statistics")
    print("❌ Type 'quit' to exit")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                summary = agent.get_session_summary(context)
                print(f"\n📊 Session Summary:")
                print(f"   Persona: {summary['current_persona']}")
                print(f"   Interactions: {summary['total_interactions']}")
                print(f"   Persona switches: {summary['persona_switches']}")
                print("\n👋 Goodbye! Thanks for using NammaAI!")
                break
                
            if user_input.lower() == 'session info':
                summary = agent.get_session_summary(context)
                print(f"\n📊 Current Session Info:")
                for key, value in summary.items():
                    print(f"   {key.replace('_', ' ').title()}: {value}")
                continue
                
            if not user_input:
                print("Please enter a message!")
                continue
                
            # Process message through agno agent
            response = agent.on_message(user_input, context)
            # Display response with persona like main.py
            current_persona = context.get('persona', None)
            detected = current_persona if current_persona and current_persona != 'unknown' else 'unknown'
            print(f"\n🧠 NammaAI ({detected}): {response}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or type 'quit' to exit.")

if __name__ == "__main__":
    run_cli()
