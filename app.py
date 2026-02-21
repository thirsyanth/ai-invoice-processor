import streamlit as st
import os
import requests
from PyPDF2 import PdfReader

st.set_page_config(page_title="AI Invoice Processor", layout="wide")

st.title("🤖 AI Invoice Processor (Gemini Powered)")
st.markdown("Upload an invoice PDF and let AI extract key details automatically.")

uploaded_file = st.file_uploader("Upload Invoice PDF", type="pdf")

if uploaded_file is not None:
    with st.spinner("Processing invoice..."):

        # Extract PDF text
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted

        # Get Gemini API Key
        api_key = os.getenv("GEMINI_API_KEY")

        # Gemini REST API Endpoint
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"

        headers = {
            "Content-Type": "application/json"
        }

        prompt = f"""
        Extract the following details from this invoice text and return ONLY valid JSON:

        - Vendor Name
        - Invoice Number
        - Invoice Date
        - Total Amount
        - Tax Amount (if available)

        Invoice Text:
        {text}
        """

        data = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

      response = requests.post(url, headers=headers, json=data)

      result = response.json()

      if response.status_code != 200:
      output = f"API Error: {result}" 
      else:
        try:
            output = result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            output = f"Parsing Error: {result}"

        st.success("✅ Invoice Processed Successfully!")
        st.subheader("📄 Extracted Data")
        st.code(output, language="json")
