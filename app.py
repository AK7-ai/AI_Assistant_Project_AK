"""
app.py

Streamlit interface for the Health Assistant.
"""

import streamlit as st

from assistant import HealthAssistant
from config import OLLAMA_BASE_URL, API_KEY



@st.cache_resource
def load_assistant():
    return HealthAssistant(
        base_url=OLLAMA_BASE_URL,
        api_key=API_KEY
    )


assistant = load_assistant()


st.set_page_config(
    page_title="Health Assistant",
    page_icon="♡",
    layout="wide"
)

st.title("Health Assistant")

st.markdown(
    """
Ask questions about the **PMData** dataset.

Examples:

- *How many steps did p01 do on 2019-11-05?*
- *What was the resting heart rate of p01 on 2019-11-05?*
- *Give me a recovery report for p01 on 2019-11-05.*
- *Compare the last two weeks of sleep.*
"""
)


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Ask a question..."):

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant answer
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            answer = assistant.ask(prompt)

        st.markdown(answer)

    # Save answer
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


    if assistant.last_tool_calls:

        with st.expander("🔧 Tool calls"):

            for tool in assistant.last_tool_calls:

                st.json(tool)

#For a side bar: 
with st.sidebar:

    st.header("About")

    st.write("**Model**")
    st.write("Llama 3.2 (Ollama)")

    st.write("**Frameworks**")
    st.write("- LangGraph")
    st.write("- OpenAI API")
    st.write("- Pydantic")
    st.write("- Pandas / NumPy")
    st.write("- Matplotlib")
    st.write("- Streamlit")

    st.write("**Dataset**")
    st.write("PMData")

    st.divider()

    if st.button("Clear conversation"):

        st.session_state.messages = []
        assistant.messages = assistant.messages[:1]

        st.rerun()
