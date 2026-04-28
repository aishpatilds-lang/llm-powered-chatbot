# AI Chatbot with Memory

This project is an AI chatbot built using Streamlit, LangChain, and Groq API.  
It can remember conversation within a session and provide context-aware responses through a simple and interactive interface.

Tech used:
- Python
- Streamlit
- LangChain
- Groq API

Features:
- Maintains conversation context (session-based memory)
- Interactive chat interface
- Real-time responses

How to run:

1. Clone the repository
git clone <your-repo-link>
cd chatbot_3

2. Create virtual environment
python -m venv venv

3. Activate environment  
Windows:
venv\Scripts\activate  
Mac/Linux:
source venv/bin/activate

4. Install dependencies
pip install -r requirements.txt

5. Add API key in `.env`
GROQ_API_KEY=your_api_key_here

6. Run the app
streamlit run app.py

Future improvements:
- Add persistent memory
- Add file upload (PDF chatbot)
- Deploy online

Author:
Aishwarya Patil