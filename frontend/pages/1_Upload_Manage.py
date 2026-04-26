import streamlit as st
import requests

API_URL = "http://localhost:8000/api"

st.set_page_config(page_title="Upload & Manage", page_icon="🗂️", layout="wide")

st.title("🗂️ Upload & Manage Documents")

if 'workspace_id' not in st.session_state:
    st.warning("Please select a workspace from the Home page first.")
    st.stop()

workspace_id = st.session_state['workspace_id']
st.caption(f"Active Workspace: **{workspace_id}**")

# --- Upload ---
st.subheader("Upload Documents")
uploaded_files = st.file_uploader("Upload PDF, TXT, or MD files", type=['pdf', 'txt', 'md'], accept_multiple_files=True)
if st.button("Upload Files") and uploaded_files:
    for file in uploaded_files:
        files = {"file": (file.name, file, file.type)}
        try:
            res = requests.post(f"{API_URL}/documents/upload?workspace_id={workspace_id}", files=files)
            if res.status_code == 200:
                st.success(f"Uploaded {file.name}")
            else:
                st.error(f"Failed to upload {file.name}: {res.text}")
        except Exception as e:
            st.error(f"Error uploading {file.name}: {e}")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Raw Documents")
    if st.button("Refresh Raw Documents"):
        pass # Streamlit reruns anyway
        
    try:
        res = requests.get(f"{API_URL}/documents?workspace_id={workspace_id}")
        if res.status_code == 200:
            docs = res.json().get("documents", [])
            if docs:
                for doc in docs:
                    st.write(f"📄 **{doc['filename']}** ({doc['category']}, {doc['size_bytes']} bytes)")
                    if st.button(f"Delete {doc['filename']}", key=f"del_{doc['filename']}"):
                        requests.delete(f"{API_URL}/documents/{doc['filename']}?workspace_id={workspace_id}")
                        st.rerun()
                
                if st.button("🚀 Ingest All Documents"):
                    with st.spinner("Ingesting documents and updating Wiki..."):
                        ingest_res = requests.post(f"{API_URL}/wiki/ingest", json={"workspace_id": workspace_id})
                        if ingest_res.status_code == 200:
                            data = ingest_res.json()
                            st.success(f"Ingest complete! Created: {data['pages_created']}, Updated: {data['pages_updated']}")
                            st.info(data['summary'])
                        else:
                            st.error(f"Ingest failed: {ingest_res.text}")
            else:
                st.info("No documents uploaded yet.")
    except Exception as e:
        st.error(f"Error fetching documents: {e}")

with col2:
    st.subheader("Wiki Operations")
    
    if st.button("🩺 Run Wiki Lint"):
        with st.spinner("Linting..."):
            res = requests.post(f"{API_URL}/wiki/lint?workspace_id={workspace_id}")
            if res.status_code == 200:
                issues = res.json().get("issues", [])
                if issues:
                    for issue in issues:
                        if issue['severity'] == "error":
                            icon = "🔴"
                        elif issue['severity'] == "suggestion":
                            icon = "💡"
                        else:
                            icon = "🟡"
                        st.write(f"{icon} **{issue['path']}**: {issue['message']}")
                else:
                    st.success("No lint issues found! Wiki is healthy.")
            else:
                st.error(f"Lint failed: {res.text}")
                
    if st.button("🔧 Repair Wiki"):
        with st.spinner("Repairing wiki... this may take a moment."):
            res = requests.post(f"{API_URL}/wiki/repair?workspace_id={workspace_id}")
            if res.status_code == 200:
                data = res.json()
                st.success(data['summary'])
                st.info(f"Pages repaired: {data['pages_repaired']} | Pages deleted: {data['pages_deleted']}")
            else:
                st.error(f"Repair failed: {res.text}")
                
    st.subheader("Wiki Pages")
    try:
        res = requests.get(f"{API_URL}/wiki/pages?workspace_id={workspace_id}")
        if res.status_code == 200:
            pages = res.json()
            if pages:
                selected_page = st.selectbox("Preview Page", pages)
                if selected_page:
                    page_res = requests.get(f"{API_URL}/wiki/page?workspace_id={workspace_id}&path={selected_page}")
                    if page_res.status_code == 200:
                        page_data = page_res.json()
                        st.markdown(f"**Frontmatter:** `{page_data['metadata']}`")
                        st.markdown(page_data['content'])
            else:
                st.info("No wiki pages yet. Run Ingest first.")
    except Exception as e:
        st.error(f"Error fetching wiki pages: {e}")
