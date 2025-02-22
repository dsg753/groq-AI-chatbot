import os
from dotenv import load_dotenv
import groq
import ipapi
from user_profile import UserProfile
import requests

load_dotenv()

client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))

def get_location():
    try:
        ip = os.getenv("USER_IP")
        location = ipapi.location(ip=ip)
        return location.get("city", "Unknown location")
    except Exception as e:
        return f"Error: {e}"

def get_weather(location):
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "Error: Weather API key missing."
    
    url = f"http://api.visualcrossing.com/elements/v1/weather/{location}?unitGroup=metric&key={api_key}&include=days"
    response = requests.get(url)
    
    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data.get("days", [{}])[0].get("temp", "Unknown temperature")
        return f"Current temperature in {location}: {temperature}°C"
    else:
        return f"Error: Unable to retrieve weather data ({response.status_code})"

def get_ai_response(user_input, user_profile):
    try:
        location = get_location()
        profile = user_profile.get_profile()
        conversation_history = profile.get("conversation_history", [])[-5:]  # Keep last 5 messages
        
        # Add the new user input to the conversation history
        conversation_history.append({"role": "user", "content": user_input})
        
        if "weather" in user_input.lower():
            weather_info = get_weather(location)
            return weather_info
        
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": f"The user is from {location} and prefers {profile['preferred_language']} language."},
                *conversation_history
            ]
        )
        
        # Add the AI response to the conversation history
        ai_response = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": ai_response})
        
        # Update user profile with the new conversation history
        user_profile.update_profile("conversation_history", conversation_history)
        
        return ai_response
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print("Welcome to dsg753 AI chatbot! Type 'exit' to quit.")
    user_id = input("Enter your user ID: ")
    user_profile = UserProfile(user_id)
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("\nGoodbye! 👋")
            break
        response = get_ai_response(user_input, user_profile)
        print("AI:", response)
