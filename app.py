# Load environment variables from .env file
# pip install streamlit langchain langchain-core
# langchain-community langchain-groq python-dotenv
import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
body {
    background-color: #0E1117;
}

/* Header */
.header {
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    color: #4CAF50;
    margin-bottom: 20px;
}

/* User bubble */
.chat-bubble-user {
    background-color: #4CAF50;
    color: white;
    padding: 12px 16px;
    border-radius: 15px;
    margin: 8px 0;
    text-align: right;
    max-width: 70%;
    margin-left: auto;
    font-size: 15px;
}

/* Bot bubble */
.chat-bubble-bot {
    background-color: #E4E6EB;
    color: black;
    padding: 12px 16px;
    border-radius: 15px;
    margin: 8px 0;
    text-align: left;
    max-width: 70%;
    font-size: 15px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- LOAD ENV --------------------
load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    st.error("❌ API key not found. Check your .env file")
    st.stop()

# -------------------- LLM --------------------
llm = ChatGroq(
    groq_api_key=os.getenv('GROQ_API_KEY'),
    model='llama-3.1-8b-instant'
)

# -------------------- PROMPT (FIXED MEMORY BEHAVIOR) --------------------
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful AI assistant. You only remember messages provided in the current session. "
     "Do not claim to recall past conversations beyond what is shown. "
     "Do not fabricate conversation history."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm

# -------------------- MEMORY --------------------
if 'store' not in st.session_state:
    st.session_state.store = {}

store = st.session_state.store

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key='input',
    history_messages_key='history'
)

# -------------------- HEADER --------------------
st.markdown('<div class="header">🤖 AI Chatbot with Memory</div>', unsafe_allow_html=True)

# -------------------- SESSION --------------------
if 'session_id' not in st.session_state:
    st.session_state.session_id = 'default'

if 'messages' not in st.session_state:
    st.session_state.messages = []

# -------------------- DISPLAY CHAT --------------------
for msg in st.session_state.messages:
    if msg['role'] == 'user':
        st.markdown(f"<div class='chat-bubble-user'>👤 {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-bot'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

# -------------------- INPUT --------------------
user_input = st.chat_input("💬 Type your message here...")

# -------------------- CHAT LOGIC --------------------
if user_input:
    st.session_state.messages.append({'role': 'user', 'content': user_input})

    with st.spinner("🤖 Thinking..."):
        response = chain_with_memory.invoke(
            {'input': user_input},
            config={'configurable': {'session_id': st.session_state.session_id}}
        )

    bot_reply = response.content

    st.session_state.messages.append({'role': 'assistant', 'content': bot_reply})

    st.rerun()

# -------------------- BUTTONS --------------------
col1, col2, col3 = st.columns(3)

# Clear Chat
with col1:
    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        store.clear()
        st.rerun()

# Show Summary
with col2:
    if st.button("📜 Show Summary"):
        summary = chain_with_memory.invoke(
            {"input": "Summarize the conversation so far briefly."},
            config={"configurable": {"session_id": st.session_state.session_id}}
        )
        st.info(summary.content)

# Session Info
with col3:
    st.info(f"Session: {st.session_state.session_id}")