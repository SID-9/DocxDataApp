import streamlit as st
import requests
import pandas as pd

#API_BASE="http://localhost:8000/api"
API_BASE="https://docxdataapp.onrender.com/api"

st.title("📄 DOCX Entity Extractor")

uploaded_file = st.file_uploader("Upload a .docx file", type=["docx"])

if uploaded_file is not None:
    if st.button("Extract Entities"):
        with st.spinner("Extracting..."):
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            }
            response = requests.post(f"{API_BASE}/extract-entities", files=files)

        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                st.error(data["error"])
            else:
                st.subheader("📘 Extracted Text")
                st.text_area("Raw Text", "\n".join(data["lines"]), height=300)

                st.subheader("🔑 Extracted Entities")
                entities = data["entities"]
                if entities:
                    df = pd.DataFrame(list(entities.items()), columns=["Entity", "Value"])
                    st.table(df)
                else:
                    st.warning("No entities extracted.")
        else:
            st.error(f"Server returned {response.status_code}")
