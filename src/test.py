import streamlit as st
import requests

# Streamlit setup
st.set_page_config(page_title="InstructAI", layout="wide")

# API details
API_BASE_URL = "http://your-api-url.com"  # Replace with your FastAPI base URL
UPLOAD_URL_ENDPOINT = "/ingestion/url"
QUERY_ENDPOINT = "/instructai/query"

# API Key (if required)
API_KEY = "your-api-key"  # Replace with your API key if needed


# CSS for light and dark themes
def apply_theme(theme):
    if theme == "Dark":
        st.markdown(
            """
            <style>
                body {
                    background-color: #1e1e1e;
                    color: white;
                }
                .stButton>button {
                    background-color: #444;
                    color: white;
                }
                .stTextInput>div>div>input {
                    background-color: #444;
                    color: white;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
    elif theme == "Light":
        st.markdown(
            """
            <style>
                body {
                    background-color: #f5f5f5;
                    color: black;
                }
                .stButton>button {
                    background-color: #ddd;
                    color: black;
                }
                .stTextInput>div>div>input {
                    background-color: white;
                    color: black;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )


# Sidebar for navigation and settings
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Query Chatbot", "URL Upload"])
theme = st.sidebar.selectbox("Select Theme", ["Light", "Dark"], index=0)

# Apply the selected theme
apply_theme(theme)

# Query Chatbot Page
if page == "Query Chatbot":
    st.title("InstructAI Chatbot")

    # Chat history container
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # User input area
    user_input = st.text_input("Write a message", placeholder="Type your message here...")

    # Function to query the API
    def query_instructai(query, session_id="default_session"):
        payload = {"query": query, "session_id": session_id}
        headers = {"x-api-key": API_KEY} if API_KEY else {}
        try:
            response = requests.post(
                API_BASE_URL + QUERY_ENDPOINT,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()  # Adjust based on your API's response format
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    # Handling user input
    if user_input:
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Query the API
        response = query_instructai(user_input)

        # Handle API response
        if "error" in response:
            ai_message = f"Error: {response['error']}"
        else:
            ai_message = response.get("response", "No response from AI.")  # Adjust based on API response

        # Add AI response to session state
        st.session_state.messages.append({"role": "assistant", "content": ai_message})

    # Display chat messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**AI:** {msg['content']}")

# URL Upload Page
elif page == "URL Upload":
    st.title("Upload URL for Ingestion")

    # Function to upload a URL
    def upload_url(url):
        payload = {"url": url}
        headers = {"x-api-key": API_KEY} if API_KEY else {}
        try:
            response = requests.post(
                API_BASE_URL + UPLOAD_URL_ENDPOINT,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()  # Adjust based on your API's response format
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    # URL input and upload button
    url_to_upload = st.text_input("Enter a URL to upload:")
    if st.button("Upload URL"):
        if url_to_upload:
            upload_response = upload_url(url_to_upload)
            if "error" in upload_response:
                st.error(upload_response["error"])
            else:
                st.success("URL uploaded successfully!")
        else:
            st.warning("Please enter a valid URL.")
