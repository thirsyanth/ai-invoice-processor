import streamlit as st
import os
from PyPDF2 import PdfReader
from openai import OpenAI

st.set_page_config(page_title="AI Invoice Processor", layout="wide")

st.title("🤖 AI Invoice Processor")
st.markdown("Upload an invoice PDF and let AI extract key details automatically.")

uploaded_file = st.file_uploader("Upload Invoice PDF", type="pdf")

if uploaded_file is not None:
    with st.spinner("Processing invoice..."):
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        prompt = f"""
        Extract the following details from this invoice text:
        - Vendor Name
        - Invoice Number
        - Invoice Date
        - Total Amount
        - Tax Amount (if available)

        Return output in JSON format.

        Invoice Text:
        {text}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an invoice data extraction assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        result = response.choices[0].message.content

        st.success("✅ Invoice Processed Successfully!")
        st.subheader("📄 Extracted Data")
        st.code(result, language="json")
