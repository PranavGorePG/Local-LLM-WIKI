import streamlit as st
import requests

API_URL = "http://localhost:8000/api"

st.set_page_config(page_title="Chat", page_icon="💬", layout="wide")

st.title("💬 Chat with Wiki")

if 'workspace_id' not in st.session_state:
    st.warning("Please select a workspace from the Home page first.")
    st.stop()

workspace_id = st.session_state['workspace_id']
st.caption(f"Active Workspace: **{workspace_id}**")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask a question about your wiki..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Searching wiki..."):
        try:
            payload = {
                "workspace_id": workspace_id,
                "history": st.session_state.messages
            }
            res = requests.post(f"{API_URL}/chat", json=payload)
            
            if res.status_code == 200:
                data = res.json()
                answer = data['answer']
                citations = data.get('citations', [])
                
                # Display assistant response
                with st.chat_message("assistant"):
                    st.markdown(answer)
                    if citations:
                        st.markdown("**Citations:**")
                        for cit in citations:
                            st.caption(f"- {cit['title']} ({cit['path']})")
                    if data.get('insight_filed'):
                        st.caption("💡 Insight filed to wiki.")
                
                # Add assistant response to history
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error(f"Error: {res.text}")
                st.session_state.messages.pop() # remove user message if failed
        except Exception as e:
            st.error(f"Connection error: {e}")
            st.session_state.messages.pop()
