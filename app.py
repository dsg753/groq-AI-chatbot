import os
from dotenv import load_dotenv
import groq
import ipapi
from user_profile import UserProfile
import requests
import time

load_dotenv()

client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))

def get_location():
    try:
        location = ipapi.location()
        return location.get("city", "Unknown location")
    except Exception as e:
        return f"Error: {e}"

def get_weather(location):
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "Error: Weather API key missing."
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?unitGroup=metric&key={api_key}&include=days"
    retries = 3
    backoff_factor = 2
    
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            weather_data = response.json()
            temperature = weather_data.get("days", [{}])[0].get("temp", "Unknown temperature")
            return f"Current temperature in {location}: {temperature}°C"
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                wait_time = backoff_factor ** attempt
                time.sleep(wait_time)
            else:
                return f"Error: Unable to retrieve weather data ({e})"

def detect_preferred_language(user_input):
    # Placeholder for language detection logic
    if any(word in user_input.lower() for word in ["hola", "gracias", "adiós"]):
        return "Spanish"
    elif any(word in user_input.lower() for word in ["bonjour", "merci", "au revoir"]):
        return "French"
    else:
        return "English"

def get_ai_response(user_input, user_profile):
    try:
        location = get_location()
        profile = user_profile.get_profile()
        conversation_history = profile.get("conversation_history", [])  # Keep entire conversation history
        
        # Add the new user input to the conversation history
        conversation_history.append({"role": "user", "content": user_input})
        
        # Detect preferred language
        preferred_language = detect_preferred_language(user_input)
        user_profile.update_profile("preferred_language", preferred_language)
        
        if "weather" in user_input.lower():
            weather_info = get_weather(location)
            return weather_info
        
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": f"The user is from {location} and prefers {preferred_language} language."},
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
