import streamlit as st
import requests
import os

API_URL = "http://localhost:8000/api"

st.set_page_config(
    page_title="LLM Wiki Local",
    page_icon="📚",
    layout="wide"
)

st.title("📚 LLM Wiki Local")
st.markdown("Welcome to your local file-based knowledge compiler.")

def get_workspaces():
    try:
        response = requests.get(f"{API_URL}/workspaces")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching workspaces: {e}")
        return []

def create_workspace(name):
    try:
        response = requests.post(f"{API_URL}/workspaces", json={"name": name})
        response.raise_for_status()
        st.success(f"Workspace '{name}' created successfully!")
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error creating workspace: {e}")
        return None

workspaces = get_workspaces()

st.subheader("Select Workspace")
if workspaces:
    workspace_names = {ws['workspace_id']: ws['name'] for ws in workspaces}
    selected_id = st.selectbox(
        "Active Workspace", 
        options=list(workspace_names.keys()), 
        format_func=lambda x: workspace_names[x]
    )
    st.session_state['workspace_id'] = selected_id
else:
    st.info("No workspaces found. Please create one.")

st.divider()

st.subheader("Create New Workspace")
with st.form("create_workspace_form"):
    new_ws_name = st.text_input("Workspace Name")
    submitted = st.form_submit_button("Create")
    if submitted and new_ws_name:
        create_workspace(new_ws_name)
        st.rerun()
