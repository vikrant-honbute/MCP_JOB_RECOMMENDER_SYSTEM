import fitz
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from apify_client import ApifyClient
load_dotenv()


llm = ChatGroq(
    model="llama3-8b-8192",
    messages=[
        {
            "role": "user",
            "content": prompt_template.format(prompt="{prompt}"),
        }
    ],
    temperature=0.5,
    api_key=os.getenv("GROQ_API_KEY"),
)


def extract_text_from_pdf(uploaded_file):
    """Extract text from a PDF file.

    Args:
        uploaded_file (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF file.
    """

    text = ""
    try:
        with fitz.open(uploaded_file) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"Error occurred while extracting text from PDF: {e}")

    return text


def ask_llm(prompt, max_tokens=500):
    """Send the prompt to the Groq LLM via LangChain and return the response."""

    prompt_template = ChatPromptTemplate.from_template("{prompt}")
    chain = prompt_template | llm
    result = chain.invoke({"prompt": prompt})
    return result.content

# # Placeholder functions for fetching jobs from LinkedIn and Naukri
# def fetch_linkedin_jobs(search_query, location="india", rows = 60):
#     run_input = {
#         "title": search_query,
#         "location": location,
#         "rows": rows,
#         "proxy": {
#             "useApifyProxy": True,
#             "apifyProxyGroups": ["RESIDENTIAL"],
#             "apifyProxyCountry": "IN",
#         }
#     }
#     run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input = run_input)
#     jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
#     return jobs

# # Placeholder function for fetching jobs from Naukri
# def fetch_naukri_jobs(search_query, location="india", rows = 60):
#     run_input = {
#         "keywords": search_query,
#         "maxJobs": 60,
#         "freshness": "all",
#         "sortBy": "relevance",
#         "experience": "all",
#     }
#     run = apify_client.actor("alpcnRV9YI9lYVPWk").call(run_input = run_input)
#     jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
#     return jobs