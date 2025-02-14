import os
from dotenv import load_dotenv
import groq
import ipapi

load_dotenv()

client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))

def get_location():
    try:
        ip = os.getenv("USER_IP")
        location = ipapi.location(ip=ip)
        return location.get("city", "Unknown location")
    except Exception as e:
        return f"Error: {e}"

def get_ai_response(user_input):
    try:
        location = get_location()
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": f"The user is from {location}."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content  
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print("Welcome to George`s AI chatbot! Type 'exit' to quit.")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("\nGoodbye! 👋")
            break
        response = get_ai_response(user_input)
        print("AI:", response)
