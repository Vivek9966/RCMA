import streamlit as st
from PyPDF2 import PdfReader
from src.graph.graph import graph
import uuid
from datetime import datetime

@st.cache_resource
def load_graph():
    return graph()
g= load_graph()

st.title("REGULATORY COMPLIANCE MONITORING AGENT (Alpha)")

uploaded_file = st.file_uploader(
    "Upload Financial documents here (.txt or .pdf )",type=['pdf','txt']
)

def extraction(file):
    if file.type == "application/pdf":
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text+= page.extract_text() or ""
        return text
    elif file.type == "text/plain":
        return file.read().decode('utf-8')
    return ''

if uploaded_file:
    text = extraction(uploaded_file)
    st.subheader("Extracted Text Preview")
    st.text_area("DOC:" , text[:1000],height=200)
    if st.button("Run Compliance Check"):
        with st.spinner("Analyzing..." , show_time=True):
              result = g.invoke({
                "input_document": text,
                "document_type": "financial",
                "compliance_questions": [],
                "retrieved_contexts": [],
                "reasoning_trace": "",
                "findings": [],
                "max_severity": "",
                "report_markdown": "",
                "audit_id": "",
                "escalated": False
            })
        report = result['report_markdown']

        st.success("completed compliance check , generated markdown file")

        st.subheader("COMPLIANCE REPORT:")
        st.markdown(report)
        st.download_button(
            label='Download',data =report,file_name=f"compliance_report_{datetime.now().strftime("%H%M%S_%d%m%y")}",mime='text/markdown'
        )