
import streamlit as st
import fitz
from google import genai

# ============================================================
# FILE SETTINGS
# ============================================================

PDF_FILE = "Impact of AI workforce Attrition.pdf"


# ============================================================
# GEMINI API KEY SETUP
# ============================================================

api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)


# ============================================================
# DASHBOARD CONTEXT
# ============================================================

dashboard_context = """
Dashboard Title:
Impact of AI adoption on workforce Attrition

Main KPIs:
- Average Productivity: 57.54
- Average Burnout Score: 50.06
- Average AI Hours: 4.23
- High Attrition Risk: 5.67%
- Task Replaced by AI: 41.25%

Task Replacement by Job Role:
- Backend Engineer: 43.5%
- Software Engineer: 43.4%
- Data Analyst: 42.6%
- Cloud Architect: 42.6%
- Data Scientist: 42.5%
- AI Ethics Officer: 42.0%
- DevOps Engineer: 42.0%

Attrition Risk by AI Adoption Stage:
- AI-First: High 6.4%, Low 48.0%, Medium 45.6%
- Experimenting: High 5.6%, Low 51.4%, Medium 43.0%
- Integrating: High 5.1%, Low 47.2%, Medium 47.8%
- Optimizing: High 6.0%, Low 47.0%, Medium 47.0%

Fear of AI Replacement:
- High: 23.87%
- Low: 34.87%
- Medium: 41.27%

High Attrition Risk Cohort by Industry:
- Automotive: Average Burnout 65.00, Average YoE 9.14, Job Satisfaction 2.47
- Consulting: Average Burnout 63.00, Average YoE 14.40, Job Satisfaction 2.72
- Cybersecurity: Average Burnout 60.78, Average YoE 8.33, Job Satisfaction 2.81
- E-commerce: Average Burnout 60.46, Average YoE 9.85, Job Satisfaction 2.65
- EdTech: Average Burnout 54.29, Average YoE 6.43, Job Satisfaction 2.83
- Fintech: Average Burnout 56.00, Average YoE 12.40, Job Satisfaction 2.88
- Gaming: Average Burnout 60.75, Average YoE 8.88, Job Satisfaction 2.60
- Total: Average Burnout 59.97, Average YoE 9.71, Job Satisfaction 2.72
"""


# ============================================================
# PDF TO IMAGE FUNCTION
# ============================================================

def render_pdf_first_page(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)

    zoom = 2.5
    matrix = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=matrix)

    return pix.tobytes("png")


# ============================================================
# GEMINI QUESTION FUNCTION
# ============================================================

def generate_answer(user_question):
    prompt = f"""
You are a senior data analyst.

You are analyzing a Power BI dashboard about AI adoption and workforce attrition.

Use only the dashboard context below.

Dashboard Context:
{dashboard_context}

User Question:
{user_question}

Instructions:
1. Answer in bullet points.
2. Keep the answer short, clear, and business-focused.
3. If the dashboard does not directly answer the question, say that clearly.
4. Give one practical recommendation.
5. Do not invent numbers outside the dashboard context.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# ============================================================
# STREAMLIT UI
# ============================================================

st.set_page_config(
    page_title="AI Workforce Attrition Dashboard",
    layout="wide"
)

st.title("End-to-End AI Workforce Attrition Dashboard Assistant")

st.markdown(
    """
This app displays a Power BI dashboard and provides a Gemini-powered Q&A section below it.
"""
)


# ============================================================
# DASHBOARD IMAGE
# ============================================================

st.markdown("## Power BI Dashboard")

try:
    dashboard_image = render_pdf_first_page(PDF_FILE)
    st.image(dashboard_image, use_container_width=True)

except FileNotFoundError:
    st.error(
        "PDF file not found. Please upload 'Impact of AI workforce Attrition.pdf' "
        "to the same folder as app.py."
    )


# ============================================================
# QUESTION SECTION
# ============================================================

st.markdown("## Ask a Question About the Dashboard")

user_question = st.text_input(
    "Enter your question:",
    placeholder="Example: Which job role has the highest AI task replacement?"
)

if st.button("Get Insights"):
    if user_question.strip():
        with st.spinner("Generating answer using Gemini API..."):
            answer = generate_answer(user_question)

        st.markdown("### Response")
        st.write(answer)
    else:
        st.warning("Please enter a question first.")
