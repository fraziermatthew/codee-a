import time
import streamlit as st
from utils import load_chain

# Custom image for the app icon and the assistant's avatar
csp_logo = 'https://apcentral.collegeboard.org/media/images/desktop/ap-computer-science-principles-192.png'
st.image('https://pbs.twimg.com/media/EUtgM_gX0AEuHmx?format=png&name=medium')

# Configure streamlit page
st.set_page_config(
    page_title="ChatCSP: ChatGPT for Computer Science Principles",
    page_icon=csp_logo
)

with st.expander("ℹ️ Disclaimer"):
    st.caption(
        "We appreciate your engagement! Please note, this is research purposes only. Thank you for your understanding."
    )

# Initialize LLM chain in session_state
if 'chain' not in st.session_state:
    st.session_state['chain']= load_chain()

# Initialize chat history
if 'messages' not in st.session_state:
    # Start with first message from assistant
    st.session_state['messages'] = [{"role": "assistant", 
                                  "content": "Hi student! I'm ChatCSP, an intelligent AI for Computer Science Principles. How can I help you today?"}]

# Display chat messages from history on app rerun
# Custom avatar for the assistant, default avatar for user
for message in st.session_state.messages:
    if message["role"] == 'assistant':
        with st.chat_message(message["role"], avatar=csp_logo):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat logic
if query := st.chat_input("Let's chat"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant", avatar=csp_logo):
        message_placeholder = st.empty()
        with st.spinner("In progress..."):
            # Send user's question to our chain
            result = st.session_state['chain']({"question": query})
            response = result['answer']
            full_response = ""

        # Simulate stream of response with milliseconds delay
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})