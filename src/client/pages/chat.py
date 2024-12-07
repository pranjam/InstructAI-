import streamlit as st
import requests
import uuid
import os

API_ENDPOINT_CHAT = f"{os.environ['BASE_URL']}/instructai/query"

def chat_bot():
    st.title("InstructAI- Chatbot!")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help?"}]
    if "id" not in st.session_state:
        st.session_state.id = str(uuid.uuid4())
    if "refs" not in st.session_state:
        st.session_state.refs = []
    if "rel_queries" not in st.session_state:
        st.session_state.rel_queries = []

    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if st.session_state.rel_queries:
        st.markdown("also search?")
    for query in st.session_state.rel_queries:
        st.button(query)
    if st.session_state.refs:
        st.markdown("References:")
    for ref in st.session_state.refs:
        st.markdown(ref)
    
    # Chat input
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # API call
        with st.chat_message("assistant"):
            payload = {"query": prompt, "session_id": st.session_state.id}
            headers = {
                    "x-api-key": os.environ["X-API-KEY"],
                    "Content-Type": "application/json",
                }
            try:
                print()
                response = requests.post(API_ENDPOINT_CHAT,headers=headers,json=payload)
                response.raise_for_status()
                response_data = response.json()
                res_ans = response_data.get("answer", "No response.")
                text = res_ans.get("answer")
                st.session_state.refs = res_ans.get("source_documents")
                st.session_state.rel_queries = res_ans.get("rel_queries")
            except requests.exceptions.RequestException as e:
                text = f"Error: {e}"

            st.markdown(text)
            st.markdown("also search?")
            for query in st.session_state.rel_queries:
                st.button(query)
            st.markdown("References:")
            for ref in st.session_state.refs:
                st.markdown(ref)
            st.session_state.messages.append({"role": "assistant", "content": text})
chat_bot()


