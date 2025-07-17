import os
import requests
from agent.agent import generate_response
import re

def get_realtime_weather(city="Bangalore"):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "[Weather API key not set. Skipping real-time weather info.]"
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api_key}&units=metric"
    
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()

        if data.get("cod") != 200:
            return f"[Weather error: {data.get('message', 'Unknown error')}]"

        desc = data['weather'][0]['description'].capitalize()
        temp = data['main']['temp']
        feels = data['main']['feels_like']
        humidity = data['main']['humidity']
        return f"Current weather in {city}: {desc}, {temp}°C (feels like {feels}°C), humidity {humidity}%."
    
    except requests.exceptions.HTTPError as http_err:
        return f"[HTTP error: {http_err}]"
    except requests.exceptions.RequestException as req_err:
        return f"[Request error: {req_err}]"
    except Exception as e:
        return f"[Error fetching weather: {e}]"


def needs_weather_info(user_input):
    weather_keywords = ["weather", "rain", "monsoon", "temperature", "forecast", "humid", "hot", "cold", "climate"]
    return any(w in user_input.lower() for w in weather_keywords)

def chat():
    print("👋 Welcome to NammaAI — Your Bangalore Smart City Concierge (with real-time weather!)")
    session_persona = None
    conversation_history = []

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! 👋")
            break

        # If weather info is needed, fetch and prepend to conversation history
        weather_info = ""
        if needs_weather_info(user_input):
            weather_info = get_realtime_weather()
            # Optionally, add to conversation history for LLM context
            conversation_history.append(f"[Weather update]: {weather_info}")

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

        # Blend weather info into the output if relevant
        if weather_info:
            print(f"\n🌦️ {weather_info}")
        print(f"\n🧠 NammaAI ({session_persona or detected}): {response}")

if __name__ == "__main__":
    chat() 