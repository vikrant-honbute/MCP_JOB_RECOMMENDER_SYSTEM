import streamlit as st
from src.helper import extract_text_from_pdf, ask_llm
from src.job_api import fetch_naukri_jobs, fetch_linkedin_jobs

st.set_page_config(page_title="MCP Job Recommender System", page_icon=":briefcase:", layout="wide")
st.title("MCP Job Recommender System")
st.markdown("Upload your resume and get personalized job recommendations from LinkedIn and Naukri.com!")

uploaded_file = st.file_uploader("Upload your resume (PDF format)", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text from the uploaded resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)
    st.success("Resume text extracted successfully!")

    with st.spinner("Summarizing your resume..."):
        summary = ask_llm(f"Summarize the following resume in a concise manner, highlighting the skills, education, and experience:\n\n{resume_text}")

    with st.spinner("Finding skill gaps..."):
        skill_gaps = ask_llm(f"Analyze this resume and highlight missing skills, certifications, and experiences needed for better job opportunities:\n\n{resume_text}")

    with st.spinner("Creating Future Roadmap..."):
        roadmap = ask_llm,(f"Based on this resume, suggest a future roadmap to improve this person's career prospects (Skill to learn, certification needed, industry exposure): \n\n{resume_text}")

    # Display nicely formatted results
    st.markdown("---")
    st.header("📑 Resume Summary")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{summary}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.header("🛠️ Skill Gaps & Missing Areas")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{skill_gaps}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.header("🚀 Future Roadmap & Preparation Strategy")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{roadmap}</div>", unsafe_allow_html=True)

    st.success("✅ Analysis Completed Successfully!")

    if st.button("🔍Get Job Recommendations🔎"):
        with st.spinner("Fetching job recommendations based on your resume..."):
            keywords = ask_llm(f"Extract the most relevant keywords from this resume that can be used for job search:\n\n{resume_text}")

            search_keywords_cleaned = keywords.replace("\n", " ").strip()

        st.success(f"Extracted Suitable Job domain : {search_keywords_cleaned}")

        with st.spinner("fetching jobs from LinkedIn and Naukari..."):
            linkedin_jobs = fetch_linkedin_jobs(search_keywords_cleaned, rows=60)
            naukri_jobs = fetch_naukri_jobs(search_keywords_cleaned, rows=60)
        st.success("Job recommendations fetched successfully!")

        st.markdown("---")
        st.header("💼 Job Recommendations from LinkedIn")

        if linkedin_jobs:
            for job in linkedin_jobs:
                st.markdown(f"**{job['title']}** at **{job['company']}** - {job['location']}")
                st.markdown(f"Posted on: {job['postedDate']} | Experience: {job['experience']} | Salary: {job.get('salary', 'N/A')}")
                st.markdown(f"[Apply Here]({job['url']})")
                st.markdown("---")
        else:
            st.info("No job recommendations found on LinkedIn based on your resume.")
        
        st.markdown("---")
        st.header("💼 Job Recommendations from Naukri.com")

        if naukri_jobs:
            for job in naukri_jobs:
                st.markdown(f"**{job['title']}** at **{job['company']}** - {job['location']}")
                st.markdown(f"Posted on: {job['postedDate']} | Experience: {job['experience']} | Salary: {job.get('salary', 'N/A')}")
                st.markdown(f"[Apply Here]({job['url']})")
                st.markdown("---")
        else:
            st.info("No job recommendations found on Naukri.com based on your resume.")
    

