import streamlit as st
import os
os.environ["BASE_URL"]= "http://localhost:8000/instructai"
from pages.chat import chat_bot
from pages.upload import upload_page


