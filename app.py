import streamlit as st
import os
import google.generativeai as genai
from PyPDF2 import PdfReader

st.set_page_config(page_title="AI Invoice Processor", layout="wide")

st.title("🤖 AI Invoice Processor (Gemini Powered)")
st.markdown("Upload an invoice PDF and let AI extract key details automatically.")

uploaded_file = st.file_uploader("Upload Invoice PDF", type="pdf")

if uploaded_file is not None:
    with st.spinner("Processing invoice..."):
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted

        # Configure Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("models/gemini-1.5-flash")

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

        response = model.generate_content(prompt)

        st.success("✅ Invoice Processed Successfully!")
        st.subheader("📄 Extracted Data")
        st.code(response.text, language="json")
