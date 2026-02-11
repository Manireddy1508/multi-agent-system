import streamlit as st
import utils
import os
import uuid
import json


st.header("Vector DB Creation", divider=True)

agents = json.loads( os.getenv("AGENTS_COLLECTION")).keys()
agent_name = st.selectbox(label="Agent", options=agents, index=None, placeholder="Select the Agent")
user_name = st.text_input(label="User Name:", placeholder="Enter the User Name")
uploaded_file = st.file_uploader(label='Please upload the file', type=['pdf', 'txt', 'mov', 'mp4', 'jpg', 'jpeg'])

if uploaded_file is not None:

    filename = uploaded_file.name
    file_extension = os.path.splitext(filename)[1].lower()  # Extract extension and lowercase

    # In case of Video and Image file needs to be stored in GCP storage.
    if file_extension in ['.mov', '.mp4', '.jpg', '.jpeg']:
        gcp_bucket_name = st.text_input(label="GCP Bucket", placeholder="Enter the GCP bucket for file upload", value="mybucket")
        
    save = st.button("Save")
    if save:
        
        temp_filename = f"temp_{uuid.uuid4()}{file_extension}"
        try:
            with st.status("Processing"):

                utils.create_temp_file(temp_filename, file_extension, uploaded_file)
                status = utils.create_document_vector(temp_filename, filename, file_extension, agent_name, user_name)
                st.balloons()

        except Exception as e:
            status= False
            error = e

        finally:
            # Removing the temp file
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

        
        # Printing File Save Status
        if status:
            st.success("Data Saved Sucessfully.")
        else:
            st.error(f"An error occurred: {error}")