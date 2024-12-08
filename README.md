# InstructAI

InstructAI is an advanced interactive chatbot designed to simplify access to and navigation of internal knowledge bases. By leveraging cutting-edge AI technologies, InstructAI enables efficient querying and retrieval of relevant documentation, promoting collaboration, learning, and transparent knowledge sharing within organizations.

## Features
- **AI-Powered Querying**: Uses Generative AI to answer user queries with contextually accurate responses.
- **Follow-Up Questions**: Understands follow-up queries without requiring the full context to be repeated.
- **Reference Links**: Provides sources for validation of the answers.
- **Three Related Questions**: Suggests additional queries to enhance exploration and understanding.
- **Modular Design**: Allows dynamic updates to prompts and configurations.

---

## Prerequisites
- Python 3.8+
- Conda (optional, but recommended for environment management)
- Streamlit (for the frontend UI)

---

## Installation and Setup

Follow these steps to clone the repository, set up the environment, and run the application:

### 1. Clone the Repository
```bash
# Clone the repository from GitHub
git clone https://github.com/yourusername/InstructAI.git
cd InstructAI
```

### 2. Create a Conda Environment
```bash
# Create a new Conda environment and activate it
conda create -n instructai_env python=3.8 -y
conda activate instructai_env
```

### 3. Install Dependencies
```bash
# Navigate to the source directory
cd src

# Install the required dependencies
pip install -r requirements.txt
```

### 4. Set Up the Environment Variables
Create a `.env` file in the `src` directory with the following variables:
```env
OPENAI_API_KEY="your_openai_api_key"
API_KEY="your_server_api_key"
PORT=8000
BASE_URL="your_server_url"
```

Replace the placeholder values with your actual API keys and server details.

---

## Running the Application

### 1. Run the Backend Server
Start the backend server to handle API requests:
```bash
python main.py
```

### 2. Run the Frontend (Streamlit)
Navigate to the client directory and start the Streamlit frontend:
```bash
cd client
streamlit run main.py
```

---

## Usage
- Open the frontend URL provided by Streamlit (usually `http://localhost:8501`) in your browser.
- Interact with the chatbot by typing queries into the input field.
- Explore follow-up questions and validate answers using the provided references.

---

## Future Enhancements
- Query enhancement for improved understanding and accuracy.
- Implement chaining for better control over multi-step queries.
- Develop custom algorithms for specialized use cases.
- Integrate with external data sources and queue systems for sitemap ingestion.

---

## License
This project is licensed under a Custom License. You are not allowed to use, modify, or distribute this project without explicit permission from the author. For inquiries, contact pranjam25@gamil.com.

---

## Acknowledgments
This project was inspired by the "build in public" philosophy of companies like GitLab, promoting transparency and collaboration.
