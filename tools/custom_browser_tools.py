import json
import requests
import streamlit as st
from pydantic import BaseModel, Field
# from unstructured.partition.html import partition_html
from crewai.tools import BaseTool

class WebsiteInput(BaseModel):
    """ Input schema for BrowserTool"""
    website: str = Field(..., description="The website URL to scrape")

class BrowserTool(BaseTool):
    name: str = "Scrape website content"
    description: str = "Useful to scrape website content"
    args_schema: type[BaseModel] = WebsiteInput

    def _run(self, website: str) -> json:
        try:
            browserless_url = f"https://chrome.browserless.io/content?token={st.secrets['BROWSERLESS_API_KEY']}" 
            payload = json.dumps({'url':website})
            headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
            response = requests.request("POST", browserless_url, headers=headers, data=payload)
            response.raise_for_status()
            return response.text
            # if response.status_code != 200:
                # return f"Failed to fetch website content. Status code: {response.status_code}"
        except Exception as e:
            return f"Error scraping website : {website}\nStatus code: {response.status_code}"
