import streamlit as st
import requests
import os

def upload(url):
    """
    Uploads a URL to the specified API endpoint.

    Args:
        url (str): The URL to be uploaded.

    Returns:
        dict: A dictionary containing the API response or an error message.
    """
    API_ENDPOINT_UPLOAD = f"{os.environ['BASE_URL']}/ingestion/url"  # Replace with your actual endpoint

    headers = {
        "x-api-key": os.environ["X-API-KEY"],
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
        if not url:
            st.error("Please provide URL.")
        else:
            response = upload(url)
            st.write("API Response:")
            st.json(response)


upload_page()