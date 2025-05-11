import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import streamlit as st
# from tools.browser_tools import BrowserTool
# from crew import AgenticRag
from crewai import LLM, Crew, Process
from Agents.mr_agents import AnalyzerAgents, StreamToExpander
from tasks.mr_tasks import AnalyzerTask
import sys



class MRCrew:
    def __init__(self, query):
        self.query = query
        self.llm = LLM(model = "openai/gpt-4o-mini")

    def run(self):
        """ Run the Crew"""
        # try:
        agents = AnalyzerAgents()
        tasks = AnalyzerTask()

        input_agent = agents.input_intent_agent()
        query_agent = agents.query_agent()
        web_agent = agents.web_retriever_agent()
        data_struct_agent = agents.data_structuring_agent()
        impact_agent = agents.impact_analyzer_agent()
        reason_agent =agents.reasoning_and_synthesis_agent()
        formatter_agent = agents.insight_formatter_agent()

        # Tasks
        input_task = tasks.input_intent_task(query = self.query, agent=input_agent)
        query_task = tasks.query_creation_task(agent=query_agent, input_intent_task=input_task)
        web_task = tasks.web_retriever_task(web_agent)
        data_task = tasks.data_structuring_task(data_struct_agent)
        impact_task = tasks.impact_analyzer_task(impact_agent)
        reason_task = tasks.reasoning_and_synthesis_task(reason_agent)
        formatter_task = tasks.insight_formatter_task(formatter_agent)

        # Crew 
        crew = Crew(
            agents = [input_agent, query_agent, web_agent,data_struct_agent,impact_agent,
                    reason_agent, formatter_agent],
            tasks= [input_task, query_task, web_task, data_task, impact_task, reason_task,formatter_task],
            verbose= True,
            process= Process.sequential
        )

        result = crew.kickoff()
        return result
        # except Exception as e:
            # print(f"An error occured - {e}")
            # return None





if __name__=="__main__":
    st.set_page_config(page_title="Competitive Intelligence Analyzer", page_icon="🕵️‍♂️", layout="wide")

    st.title("🧠 Competitive Intelligence Agent")
    st.subheader("Analyze your competitor's moves like a pro.")

    input_ = st.text_input("🔍 Enter a Company or Organization Name with your intent for analyzing", placeholder="e.g., Tesla,Razorpay")
    if st.button("Run Analysis"):
        if input_.strip() == "":
            st.warning("Please enter a valid company name and query.")
        else:
            # with st.spinner(f"Running Agentic RAG analysis..."):
                # try:
                #     result = AgenticRag(query = company)  # This should return a final summary or structured output
                #     st.success("✅ Analysis Complete!")
                #     st.subheader("📊 Intelligence Summary")
                #     st.markdown(result)
                # except Exception as e:
                #     st.error(f"🚨 Something went wrong: {e}")

                # result = AgenticRag(query = company)  # This should return a final summary or structured output
            with st.status("🤖 **Agents at work...**", state="running", expanded=True) as status:
                with st.container(height=500, border=False):
                    sys.stdout = StreamToExpander(st)
                    market_research =MRCrew(input_) 
                    result = market_research.run()
                status.update(label="✅ Market Research Analysis Complete!!",
                                state="complete", expanded=False)
            st.subheader("📊 Intelligence Summary", anchor=False, divider="rainbow")
            st.markdown(result)

