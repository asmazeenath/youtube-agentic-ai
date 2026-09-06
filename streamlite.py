import streamlit as st

from google.adk.runners import InMemoryRunner
from google.genai import types
from dotenv import load_dotenv
load_dotenv()
import asyncio

from finance_assistance_agent.agent import root_agent


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI Finance Assistant",
    page_icon="💰",
    layout="centered"
)


# -----------------------------
# Header
# -----------------------------

st.title("💰 AI Finance Assistant")

st.write(
    "Your personal AI assistant for budgeting, saving "
    "and financial planning."
)


# -----------------------------
# Initialize Session
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


if "runner" not in st.session_state:

    st.session_state.runner = InMemoryRunner(
        agent=root_agent,
        app_name="finance_assistant"
    )


if "session_id" not in st.session_state:

    session = asyncio.run(st.session_state.runner.session_service.create_session(
        app_name="finance_assistant",
        user_id="user"
    ))
    st.session_state.session_id = session.id

# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.header("💡 Finance Assistant")

    st.write("You can ask me:")

    st.markdown("""
    💰 **Savings**
    
    📊 **Expense Analysis**
    
    🎯 **Financial Goals**
    
    📈 **Stock Prices**
    
    📰 **Market News**
    
    🏦 **Investment Information**
    """)

    st.divider()

    st.subheader("Example Questions")

    st.write("• How can I save more money?")

    st.write("• Analyse my expenses")

    st.write("• Create a saving plan")

    st.write("• What is Tesla's latest stock price?")

    st.write("• What is the latest market news?")

    st.divider()

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()


# -----------------------------
# Display Chat History
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# -----------------------------
# User Input
# -----------------------------

user_input = st.chat_input(
    "Ask something about your finances..."
)


if user_input:

    # Show user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):

        st.markdown(user_input)


    # -------------------------
    # AI Response
    # -------------------------

    with st.chat_message("assistant"):

        with st.spinner("🤔 Thinking..."):

            try:

                content = types.Content(
                    role="user",
                    parts=[
                        types.Part(
                            text=user_input
                        )
                    ]
                )


                response_text = ""

                events = st.session_state.runner.run(
                    user_id="user",
                    session_id=st.session_state.session_id,
                    new_message=content
                )


                for event in events:

                    if event.is_final_response():

                        if event.content and event.content.parts:

                            for part in event.content.parts:

                                if part.text:

                                    response_text += part.text


                if not response_text:

                    response_text = (
                        "Sorry, I couldn't generate a response."
                    )


            except Exception as e:

                response_text = f"❌ Error: {str(e)}"


            st.markdown(response_text)


    # Save response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response_text
        }
    )