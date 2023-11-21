from agents import Agent
from openai import OpenAI
import streamlit as st
import html

with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Key", key="chatbot_api_key", type="password"
    )
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/Hornet47/Tetra)"

st.title("💬 TETRA")
st.caption("🚀 A streamlit chatbot powered by OpenAI Assistant")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key).beta
    tetra = Agent(
        client=client,
        tools=[
            {"type": "code_interpreter"}
        ],
    )
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    msg = tetra.process_message(prompt)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(html.escape(msg))
