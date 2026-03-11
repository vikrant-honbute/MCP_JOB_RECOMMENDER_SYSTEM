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
        roadmap = ask_llm(f"Based on this resume, suggest a future roadmap to improve this person's career prospects (Skill to learn, certification needed, industry exposure): \n\n{resume_text}")

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
            keywords = ask_llm(
                f"From the resume below, return ONLY a short comma-separated list of the top 5 job title keywords "
                f"suitable for a job search query (e.g. 'AI Engineer, Data Scientist, ML Engineer'). "
                f"Do not include any explanation or extra text.\n\n{resume_text}"
            )

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
                title = job.get('title', 'N/A')
                company = job.get('company', job.get('companyName', 'N/A'))
                location = job.get('location', 'N/A')
                posted = job.get('postedDate', job.get('postedAt', 'N/A'))
                experience = job.get('experience', 'N/A')
                salary = job.get('salary', 'N/A')
                url = job.get('url', job.get('link', '#'))
                st.markdown(f"**{title}** at **{company}** - {location}")
                st.markdown(f"Posted on: {posted} | Experience: {experience} | Salary: {salary}")
                st.markdown(f"[Apply Here]({url})")
                st.markdown("---")
        else:
            st.info("No job recommendations found on LinkedIn based on your resume.")
        
        st.markdown("---")
        st.header("💼 Job Recommendations from Naukri.com")

        if naukri_jobs:
            for job in naukri_jobs:
                title = job.get('title', job.get('jobTitle', 'N/A'))
                company = job.get('company', job.get('companyName', 'N/A'))
                location = job.get('location', job.get('placeholders', [{}])[0].get('label', 'N/A') if isinstance(job.get('placeholders'), list) else 'N/A')
                posted = job.get('postedDate', job.get('footerPlaceholderLabel', 'N/A'))
                experience = job.get('experience', 'N/A')
                salary = job.get('salary', job.get('placeholders', [{}])[1].get('label', 'N/A') if isinstance(job.get('placeholders'), list) and len(job.get('placeholders', [])) > 1 else 'N/A')
                url = job.get('url', job.get('jdURL', '#'))
                if url and not url.startswith('http'):
                    url = 'https://www.naukri.com' + url
                st.markdown(f"**{title}** at **{company}** - {location}")
                st.markdown(f"Posted on: {posted} | Experience: {experience} | Salary: {salary}")
                st.markdown(f"[Apply Here]({url})")
                st.markdown("---")
        else:
            st.info("No job recommendations found on Naukri.com based on your resume.")
    

