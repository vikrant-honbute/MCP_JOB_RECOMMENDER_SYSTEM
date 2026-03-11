
from apify_client import ApifyClient
import os
from dotenv import load_dotenv
load_dotenv()

apify_client = ApifyClient(os.getenv("APIFY_API_KEY"))

# Placeholder functions for fetching jobs from LinkedIn and Naukri
def fetch_linkedin_jobs(search_query, location="india", rows = 60):
    run_input = {
            "title": search_query,
            "location": location,
            "rows": rows,
            "proxy": {
                "useApifyProxy": True,
                "apifyProxyGroups": ["RESIDENTIAL"],
                "apifyProxyCountry": "IN",
            }
    }
    run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input = run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs

# Placeholder function for fetching jobs from Naukri
def fetch_naukri_jobs(search_query, location="india", rows = 60):
    run_input = {
            "keywords": search_query,
            "maxJobs": 60,
            "freshness": "all",
            "sortBy": "relevance",
            "experience": "all",
        }
    run = apify_client.actor("alpcnRV9YI9lYVPWk").call(run_input = run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs