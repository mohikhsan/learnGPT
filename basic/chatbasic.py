import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Add openAI key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# List to store chat messages between user and openAI
messages = [] 

# Set up openAI system by prompting it with a few sentences
# Example: "I am a highly trained football coach that can give you advice on how to effectively train as a footballer."
system_msg = input("Describe the type of chatbot you want to create: ")
messages.append({"role": "system", "content": system_msg})

# Confirm bot setup
print("You have set up your chatbot as: " + system_msg)

while input != "quit()":
    # Prompt for input from user
    message = input("You: ")
    messages.append({"role": "user", "content": message})

    # Send message to openAI and get response
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=messages)

    # Print response from openAI, add response to messages list
    reply = response["choices"][0]["message"]["content"]
    print("Bot: " + reply + "\n")
    messages.append({"role": "assistant", "content": reply})
