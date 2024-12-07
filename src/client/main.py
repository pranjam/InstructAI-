import streamlit as st
import os
from dotenv import load_dotenv
# Load environment variables from a .env file
load_dotenv()
from pages.chat import chat_bot
from pages.upload import upload_page


