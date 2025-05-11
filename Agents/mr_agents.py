from crewai import Agent
from crewai import LLM
from tools.browser_tools import BrowserTools
import re
import streamlit as st

class AnalyzerAgents():
    def __init__(self, llm=None):
        if llm is None:
            # self.llm = LLM(model = "groq/gemma2-9b-it")
            # self.llm = LLM(model = "gemini/gemini-2.0-flash")
            # self.llm = LLM(model = "gemini/gemini-pro")
            self.llm = LLM(model = "openai/gpt-4o-mini" )
        else:
            self.llm = llm
        # Intialize Tools once and for all If exists
        self.browser_tools = BrowserTools.browser_tool
        self.website_search_tools = BrowserTools.website_tool
    
    def input_intent_agent(self):
        return Agent(
            role =f"Understand the request's intent from the user's natural language input query. ",
            goal = "Classify and extract structured information from the user's natural language input " \
                    "to determine the nature of the competitive intelligence request.",
            backstory= """You are a seasoned market research strategist who has spent over a decade helping companies gain
                        an edge by deeply understanding their competitive landscape.
                        You are skilled in discerning what stakeholders/executives really want - be it pricing intel, product comparison, partnership analysis,
                        or market entry feasibility just from a few lines of input.
                        Your expertise lies in deconstructing vague queries and shaping them into a clear research plan for downstream agents.""",
            llm= self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def query_agent(self):
        return Agent(
            role = "Transform structured competitive intelligence intents into effective, multi-angle search queries that maximize relevant retrieval from both structured (e.g., APIs, databases) and unstructured (e.g., web, news) sources.",
            goal = 
                """ Use structured input from the Input Understanding Agent.
                    Craft diverse and rich queries using:
                    1. Synonym expansion ("pricing model" → "transaction fees", "cost structure")
                    2. Boolean logic (AND, OR)
                    3. Site targeting (site:crunchbase.com, site:techcrunch.com)
                    4. Time filtering (e.g., "2024", "last 6 months")
                    Support different retrieval backends (web search, vector DBs, APIs).
                    Return multiple queries targeting different angles.""",
  
            backstory = 
                        """You are a former investigative journalist turned competitive intelligence analyst, known for your uncanny ability to ask the right questions to get to the bottom of any market trend or competitor move. 
                            You're fluent in search engine behavior, API quirks, and information retrieval hacks. You craft nuanced and strategic queries that leave no stone unturned—whether it's pricing models, executive interviews, or obscure partnership news. 
                            You're the one others come to when Google just isn’t enough.""",
                llm= self.llm,
                verbose=True,
                allow_delegation=False
                    )
    
    def web_retriever_agent(self):
        return Agent(

            role = "Retrieve relevant documents, news, or structured data from the web, APIs, or internal knowledge sources using the queries generated.",
            goal = 
                """ Run search queries (via APIs).
                    Collect top N URLs and snippets or full documents.
                    Optionally classify them by source credibility or topic.""",
  
            backstory = 
                        """You are a research librarian turned data miner, fluent in scraping, crawling, and deep search. You've worked with hedge funds, governments, and newsrooms to uncover buried intel. 
                            You don't just retrieve—you curate relevance with surgical precision.""",
            llm= self.llm,
            verbose=True,
            tools= [self.browser_tools],
            allow_delegation=False
            )
    
    def data_structuring_agent(self):
        return Agent(

            role = "Extract structured entities and relationships from unstructured web text (e.g., partnerships, dates, pricing, metrics).",
            goal = 
                """ Use NER, regex, or LLMs to extract structured info
                    Normalize company names, dates, events
                    Tag and group similar information""",
  
            backstory = 
                        """A former data journalist, you've spent years converting messy press releases and product pages into clean datasets for decision-makers. 
                            Where others see noisy paragraphs, you see JSON-ready intelligence.""",
            llm= self.llm,
            verbose=True,
            tools= [self.browser_tools],
            allow_delegation=False
            )
    
    def impact_analyzer_agent(self):
        return Agent(
            role = "Assess the sentiment, tone, and strategic significance of events or actions mentioned in the retrieved documents.",
            goal = 
                """ Perform sentiment classification (positive, neutral, negative)
                    Identify impact level: high/medium/low
                    Assign business significance (e.g., "affects growth", "improves cost efficiency")""",
  
            backstory = 
                        """You're a seasoned market strategist and former equity analyst. You don’t just read headlines—you dissect tone, infer implications, and spot strategic shifts buried between the lines. 
                            You were trained to see what others ignore.""",
            llm= self.llm,
            tools= [self.browser_tools],
            verbose=True,
            allow_delegation=False
            )

    def reasoning_and_synthesis_agent(self):
        return Agent(
            role = "Integrate findings into a cohesive, strategic insight or narrative suitable for business decision-making.",
            goal = 
                """ Compare competitors side-by-side.
                    Highlight implications, patterns, contradictions
                    Answer the "So what?" question""",
  
            backstory = 
                        """You are a McKinsey-trained strategy advisor with deep tech domain experience. 
                            You can take a dozen market signals and convert them into one powerful recommendation. 
                            You are not just summarizing—you’re strategizing.""",
            llm= self.llm,
            verbose=True,
            tools= [self.browser_tools],
            allow_delegation=False
            )
    
    def insight_formatter_agent(self):
        return Agent(
            role = "Present the final insights in the required format: a battlecard, report, email digest, etc., tailored for specific users.",
            goal = 
                """ Convert raw text to structured output
                    Support multiple templates (SWOT, bullet points, summary, slide content)
                    Improve readability and brevity""",
  
            backstory = 
                        """You're a former Deloitte consultant and presentation coach. 
                           You've crafted countless pitch decks, reports, and market updates for CXOs. 
                            You translate intelligence into influence with clarity and visual structure.""",
            llm= self.llm,
            verbose=True,
            allow_delegation=False
            )

class StreamToExpander:
    def __init__(self, expander):
        self.expander = expander
        self.buffer = []
        self.colors = ['red', 'green', 'blue', 'orange']
        self.color_index = 0

    def write(self, data):
        # Filter out ANSI escape codes using a regular expression
        cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)

        # Check if the data contains 'task' information
        task_match_object = re.search(r'\"task\"\s*:\s*\"(.*?)\"', cleaned_data, re.IGNORECASE)
        task_match_input = re.search(r'task\s*:\s*([^\n]*)', cleaned_data, re.IGNORECASE)
        task_value = None
        if task_match_object:
            task_value = task_match_object.group(1)
        elif task_match_input:
            task_value = task_match_input.group(1).strip()

        if task_value:
            st.toast(":robot_face: " + task_value)

        # Check if the text contains the specified phrase and apply color
        if "Entering new CrewAgentExecutor chain" in cleaned_data:
            self.color_index = (self.color_index + 1) % len(self.colors)
            cleaned_data = cleaned_data.replace("Entering new CrewAgentExecutor chain", 
                                              f":{self.colors[self.color_index]}[Entering new CrewAgentExecutor chain]")

        if "City Selection Expert" in cleaned_data:
            cleaned_data = cleaned_data.replace("City Selection Expert", 
                                              f":{self.colors[self.color_index]}[City Selection Expert]")
        if "Local Expert at this city" in cleaned_data:
            cleaned_data = cleaned_data.replace("Local Expert at this city", 
                                              f":{self.colors[self.color_index]}[Local Expert at this city]")
        if "Amazing Travel Concierge" in cleaned_data:
            cleaned_data = cleaned_data.replace("Amazing Travel Concierge", 
                                              f":{self.colors[self.color_index]}[Amazing Travel Concierge]")
        if "Finished chain." in cleaned_data:
            cleaned_data = cleaned_data.replace("Finished chain.", 
                                              f":{self.colors[self.color_index]}[Finished chain.]")

        self.buffer.append(cleaned_data)
        if "\n" in data:
            self.expander.markdown(''.join(self.buffer), unsafe_allow_html=True)
            self.buffer = []

    def flush(self):
        """Flush the buffer to the expander"""
        if self.buffer:
            self.expander.markdown(''.join(self.buffer), unsafe_allow_html=True)
            self.buffer = []

    def close(self):
        """Close the stream"""
        self.flush()