# Groq AI Chatbot

🤖 A simple terminal-based AI chatbot built with Python and Groq. It uses the Groq API to generate responses based on user inputs.

## Features

- **AI Responses**: The chatbot uses the Groq API to generate responses based on user inputs.
- **User Interaction**: Continuous user interaction until the user types "exit" or "quit" to exit.
- **Error Handling**: Graceful handling of API errors.

## How to Run

You need Python 3.x installed on your system.

1. Clone the repository:
    
    git clone https://github.com/dsg753/groq-AI-chatbot.git
    cd groq-AI-chatbot
    

2. Install the required packages:
    # install from PyPI
pip install groq

3. Create a `.env` file in the root of the project and add your Groq API key:
    
    GROQ_API_KEY=your_groq_api_key
    

4. Run the chatbot:
    
    python app.py
    

## Environment Variables

Make sure to add the following environment variable in your `.env` file:
- `GROQ_API_KEY`: Your API key for the Groq API.

## License

This project is licensed under the MIT License.
