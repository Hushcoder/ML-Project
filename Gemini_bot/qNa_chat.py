import google.generativeai as genai
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# function to load gemini pro model and get response

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])


def gemini_response(query):
    response = chat.send_message(query, stream=True)
    return response


# initialise stremalit app

st.set_page_config(page_title="QnA Interface")
st.header("Gemini LLM")

# Initialise session state for chat history if not exixts

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input:", key="input")
submit = st.button("Submit & Edit")

if submit and input:
    response = gemini_response(input)
    # Add user query and response to session chat history
    st.session_state['chat_history'].extend(("You: ", input))
    st.subheader("Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].extend(("Bot: ", chunk.text))
st.subheader("CHAT HISTORY")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")
