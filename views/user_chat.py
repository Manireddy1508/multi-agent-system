import streamlit as st
from langchain_openai import ChatOpenAI
import json
import uuid
from datetime import datetime, timezone

from models.chat import ChatMessage
from storage.firestore import FirestoreService
firestoreService = FirestoreService()

def load_json(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data


if "messages" not in st.session_state:
    st.session_state.messages = []

if "llm" not in st.session_state:
    st.session_state.llm = ChatOpenAI(model="gpt-4.1-nano")

if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # if "files" in message:
        #     st.image(message["files"][0])


user_query = st.chat_input(
    "Say something and/or attach an image",
    accept_file=True,
    # file_type=["jpg", "jpeg", "png"],
)

if user_query and user_query.text and (not user_query["files"]):

    with st.chat_message("user"):
        st.markdown(user_query.text)
    st.session_state.messages.append({"role": "user", "content": user_query.text})

    # Loading prompt
    prompt = "system:" + load_json("./agent_prompts/commerce_growth.json")["prompt"]

    # Append user query to the prompt along with chat history
    prompt += "\n ".join([f"{message['role']}: {message['content']}" for message in st.session_state.messages])
    prompt+= "\n user: " + user_query.text

    # Invoke the LLM with the constructed prompt    
    with st.spinner("Thinking..."):
        response = st.session_state.llm.invoke(prompt)

    with st.chat_message("assistant"):
        st.markdown(response.content)
    st.session_state.messages.append({"role": "assistant", "content": response.content})


# if user_query and user_query["files"]:
#     with st.chat_message("user"):
#         st.image(user_query["files"][0])
#         st.markdown(user_query.text)
#     st.session_state.messages.append({"role": "user", "content": user_query.text, "files": user_query["files"]})

#     response = f"Echo: {user_query.text}"
#     with st.chat_message("assistant"):
#         st.markdown(response)
#     st.session_state.messages.append({"role": "assistant", "content": response})


    # Save chat history to Firestore
    firestoreService.save_chat_history(
        user_id = "user_id_placeholder",  # Replace with actual user ID
        agent_id = "commerce_growth",  # Replace with actual agent ID
        chat_id = st.session_state.chat_id,
        messages = [
            ChatMessage(
                role=message['role'],
                content=message['content']
            )
            for message in st.session_state.messages
        ]
    )
