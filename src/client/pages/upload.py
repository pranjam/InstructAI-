import streamlit as st
import requests
import os

def upload(x_api_key, url):
    """
    Uploads a URL to the specified API endpoint.

    Args:
        x_api_key (str): The API key for authentication.
        url (str): The URL to be uploaded.

    Returns:
        dict: A dictionary containing the API response or an error message.
    """
    API_ENDPOINT_UPLOAD = f"{os.environ['BASE_URL']}/url"  # Replace with your actual endpoint

    headers = {
        "x-api-key": "5646cf54-c2b3-466e-8185-a55d1a8c921e",
        "Content-Type": "application/json",
    }

    payload = {"url": url}

    try:
        response = requests.post(API_ENDPOINT_UPLOAD, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def upload_page():
    # Streamlit UI elements
    st.title("URL Upload to API")    
    # URL input
    url = st.text_input("Enter the URL to upload")
    
    if st.button("Upload URL"):
        if not x_api_key or not url:
            st.error("Please provide both the API key and URL.")
        else:
            response = upload(x_api_key, url)
            st.write("API Response:")
            st.json(response)


upload_page()