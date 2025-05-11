
# Importing crewAI tools
from crewai_tools import (
    SerperDevTool,
    WebsiteSearchTool
)


class BrowserTools:
    browser_tool = SerperDevTool()
    website_tool = WebsiteSearchTool()