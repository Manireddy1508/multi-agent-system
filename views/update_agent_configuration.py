import streamlit as st
import utils
import os
import uuid
import json

st.header("Modify Agent Configuration ", divider=True)


# Function to load JSON data from a file
def load_json(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data

# Function to save JSON data to a file
def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def find_json_files(root_dir):
    """Recursively finds all .json files in a directory."""
    json_files = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".json"):
                agent_name = filename.split('.')[0]  # Extract agent name from filename
                json_files[agent_name] = os.path.join(dirpath, filename)
    return json_files


root_dir = "./agent_prompts"  # Current directory

# Find all JSON files
json_files = find_json_files(root_dir)


selected_file = st.selectbox("Select Agent:", list(json_files.keys()))

try:
    data = load_json(json_files[selected_file])
except FileNotFoundError:
    st.error(f"Error: File not found at {selected_file}")
except json.JSONDecodeError:
    st.error(f"Error: Invalid JSON format in {selected_file}")
except Exception as e:
    st.error(f"An error occurred: {e}")

updated_value = st.text_area(label="Agent_1", value=list(data.values())[0], height=150)

# Save button
if st.button("Save Changes"):
    data["prompt"] = updated_value
    save_json(json_files[selected_file], data)
    st.success("Changes saved to prompt.json")
    # To reflect the changes immediately, you can rerun the script

if st.button("Reload"):
    st.rerun()
