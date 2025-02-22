import streamlit as st
import requests

LLM_API_URL = "http://manage_gym_llm:8001/chat"

def chatbot_page():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #111111 !important;
        }

        .header-container {
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #1e1e1e;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            width: 100%;
        }

        .header-text {
            font-size: 28px !important;
            font-weight: bold !important;
            color: white !important;
            text-align: center !important;
        }

        .question-label-container {
            background-color: #1e1e1e !important;
            color: white;
            font-size: 20px !important;
            font-weight: bold !important;
            padding: 10px !important;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 10px !important;
        }

        .question-box {
            background-color: #222 !important;
            color: #ffffff !important;
            font-weight: bold !important;
            padding: 10px !important;
            border-radius: 10px !important;
            margin-bottom: 10px !important;
        }

        .response-box {
            background-color: #1e1e1e;
            color: #ffffff;
            padding: 15px;
            border-radius: 8px;
            font-size: 20px !important;
            margin-top: 10px;
        }

        .stButton>button {
            background-color: #444 !important;
            color: white !important;
            border-radius: 5px;
            font-weight: bold !important;
            padding: 8px 15px;
            font-size: 16px !important;
        }

        .stTextInput>div>div>input {
            background-color: #222 !important;
            color: white !important;
            border-radius: 5px !important;
            font-size: 18px !important;
            padding: 10px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="header-container">
            <span class="header-text">💬 AI Chat Assistant - FitMe 💬</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 4, 1])

    with col2:
        st.markdown("<div class='question-label-container'>🤖 Ask the AI something about fitness 🤖:</div>", unsafe_allow_html=True)
        user_input = st.text_input(" ", key="user_input")

        if st.button("Send"):
            if user_input:
                response = requests.post(
                    LLM_API_URL,
                    json={"prompt": user_input, "context": "User query from frontend"}
                )

                if response.status_code == 200:
                    result = response.json().get("response", "No response received.")

                    st.markdown(f"<div class='question-box'>🧑‍💻 **You:** {user_input}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='response-box'>🤖 **AI:** {result}</div>", unsafe_allow_html=True)
                else:
                    st.error("⚠️ Error communicating with the AI. Please try again.")
            else:
                st.warning("⚠️ Please enter a question.")
