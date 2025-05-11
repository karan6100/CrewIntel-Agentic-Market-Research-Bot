from crewai import Agent,Task, Crew, Process,LLM
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import SerperDevTool, PDFSearchTool
from Agentic_RAG_CrewAI.intelligence_analyst_rag_crewai.tools.custom_browser_tools import BrowserTool
from dotenv import load_dotenv
import os
import yaml

# API keys
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["BROWSERLESS_API_KEY"] = os.getenv("BROWSERLESS_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

# intitalize tools
# web_search_tool = SerperDevTool()
web_search_tool = BrowserTool()


@CrewBase
class AgenticRag():
    """Agentic RAG Crew"""

    def __init__(self, query):

        self.agents_config_path = "config/agents.yaml"
        self.tasks_config_path = "config/tasks.yaml"

        self.llm = LLM("openai/gpt-4o",
                       temperature=0.3)
        self.query = query

        # Load YAML files as dictionaries
        with open(self.agents_config_path, "r") as f:
            self.agents_config = yaml.safe_load(f)
        
        with open(self.tasks_config_path, "r") as f:
            self.tasks_config = yaml.safe_load(f)
        
        

    @agent
    def input_agent(self, query: str) -> Agent:

        agent_config = self.agents_config["input_intent_agent"]
        formatted_agent = {
            "role": agent_config["role"].format(query=self.query),
            "goal": agent_config["goal"],
            "backstory": agent_config["backstory"]
        }
        return Agent(
            config=formatted_agent,
            verbose=True,
            llm=self.llm
        )

    @task
    def input_task(self, query: str) -> Task:

        task_config = self.tasks_config["input_intent_task"]
        formatted_task = {
            "role": task_config["description"].format(query=self.query)
        }
        return Task(
            config=formatted_task
        )


        # return Task(
        #     config=self.tasks_config["input_intent_task"].format(query = self.query)
        # )
    


    @agent
    def query_agent(self) -> Agent:
        return Agent(
            config= self.agents_config['query_agent'],
            verbose=True,
            tools = [web_search_tool],
            llm = self.llm
        )
    @task
    def query_task(self) -> Task:
        return Task(
            config=self.tasks_config["query_creation_task"]

        )
    

    
    @agent
    def web_retriever_agent(self) -> Agent:
        return Agent(
            config= self.agents_config['web_retriever_agent'],
            verbose=True,
            tools = [web_search_tool],
            llm = self.llm
        )
    @task
    def web_retriever_task(self) -> Task:
        return Task(
            config=self.tasks_config["web_retriever_task"]

        )
    

    @agent
    def data_structuring_agent(self) -> Agent:
        return Agent(
            config= self.agents_config['data_structuring_agent'],
            verbose=True,
            tools = [web_search_tool],
            llm = self.llm
        )
    @task
    def data_structuring_task(self) -> Task:
        return Task(
            config=self.tasks_config["data_structuring_task"]

        )
    

    @agent
    def impact_analyzer_agent(self) -> Agent:
        return Agent(
            config= self.agents_config['impact_analyzer_agent'],
            verbose=True,
            llm = self.llm
        )
    @task
    def impact_analyzer_task(self) -> Task:
        return Task(
            config=self.tasks_config["impact_analyzer_task"]

        )
    
    @agent
    def reasoning_and_synthesis_agent(self) -> Agent:
        return Agent(
            config= self.agents_config['reasoning_and_synthesis_agent'],
            verbose=True,
            llm = self.llm
        )
    @task
    def reasoning_and_synthesis_task(self) -> Task:
        return Task(
            config=self.tasks_config["reasoning_and_synthesis_task"]

        )
    
    @agent
    def insight_formatter_agent(self) -> Agent:
        return Agent(
            config= self.agents_config['insight_formatter_agent'],
            verbose=True,
            llm = self.llm
        )
    @task
    def insight_formatter_task(self) -> Task:
        return Task(
            config=self.tasks_config["insight_formatter_task"],
            output_file= "output/analysis.md"
        )
    
    @crew
    def crew(self) -> Crew:
        """ Creates AgenticRag Crew"""
        return Crew(
            agents = self.agents,
            tasks= self.tasks,
            process= Process.sequential,
            verbose= True

        )

