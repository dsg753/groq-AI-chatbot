# dsg753 AI Chatbot

🤖 This is an AI chatbot application using Groq's API and `ipapi-py` to provide location-based responses.

## Features

- User Profile Management
- Location Detection
- Weather Information
- Language Detection
- AI-Powered Conversations
- Error Handling
- Environment Configuration
- Interactive Command-Line Interface

## IPAPI Integration

The chatbot uses `ipapi-py` to determine the user's location based on their IP address. This information is included in the context provided to the AI model, allowing it to generate more personalized responses.

## Environment Configuration

Create a `.env` file in the root directory of the project with the following content:

```
GROQ_API_KEY=your_groq_api_key
WEATHER_API_KEY=your_weather_api_key
```

Replace `your_groq_api_key` and `your_weather_api_key` with your actual API keys.

## Installation

Install the required dependencies using the following command:

```sh
pip install -r requirements.txt
```

## Running the Chatbot

Run the chatbot using the following command:

```sh
python app.py
```

Type 'exit' to quit the chatbot.
```

## License

This project is licensed under the MIT License.
