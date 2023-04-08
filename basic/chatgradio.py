import gradio as gr
import openai
import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# Add openAI key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initiate List to store chat messages between user and openAI
# Bot character is setup through environment variable
messages = [{"role": "system", "content": os.getenv("OPENAI_BOT_PERSONA")}]

# function to communicate with openAI
def connect_to_openai(user_input):
    global messages

    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    openai_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": openai_reply})

    return openai_reply

# callback for user input
def user(user_message, history):
    return "", history + [[user_message, None]]

# callback for openAI response
def bot(history):
        bot_message = connect_to_openai(history[-1][0])
        history[-1][1] = bot_message
        return history

# callback for clear button
def clearChat(history):
    global messages

    messages.clear()
    messages.append({"role": "system", "content": os.getenv("OPENAI_BOT_PERSONA")})
    print(messages)
    
    return None

# build graido interface
with gr.Blocks() as demo:
     # create the header
    gr.Markdown(
        """
    # Kinna AI
    ## Asisten Parenting berbasis AI
    """
    )

    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Tanya Kinna", placeholder="Ketik disini...")
    clear = gr.Button("Mulai Ulang")

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear.click(clearChat, None, chatbot, queue=False)

demo.launch(share=False)

