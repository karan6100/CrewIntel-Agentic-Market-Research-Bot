from crewai import Task

class AnalyzerTask():
    def __validate_inputs(self, query):
        """Validaes if all inputs are provided else raise an error"""
        if not query:
            raise ValueError("All input parameters not provided")
        return True
    
    def input_intent_task(self, query, agent):
        self.__validate_inputs(query)
        return Task( 
                name = "input_intent_task",
                description= f"Understand and classify the user's intent, extract key entities (companies, focus areas, regions), and generate a structured JSON plan for the rest of the crew for given query {query}",
                agent = agent,
                expected_output="""A structured JSON object with fields: 
                                    - intent (string)
                                    - target_companies (list)
                                    - focus_areas (list)
                                    - region (optional, string)
                                    - time_range (optional, e.g., 'past 6 months')"""
        )
    
    def query_creation_task(self, agent, input_intent_task):
        return Task( 
                name = "query_creation_task",
                description= """
                            Generate multiple well-formed search queries to retrieve relevant data based on the user's structured request. 
                            Use variations in phrasing, synonyms, site filters (like site:techcrunch.com), time filters (e.g., '2024', 'last 6 months'), and include all companies and focus areas.
                            Ensure queries are appropriate for web search or retrieval APIs.
                            Output a JSON list of query strings, with optional metadata like source type or priority.
                            """,
                agent = agent,
                context = [input_intent_task], # This task will wait for input_intent_task to complete
                expected_output="""{
                                    "query_type": "web",
                                    "queries": [... ]
                                    }
                                    """       
        ) 
    
    def web_retriever_task(self, agent):
        return Task( 
                name = "web_retriever_task",
                description= """Search the web using the queries provided. Return top 3–5 relevant snippets or full-text results per query. 
                                Focus on recency and relevance.""",
                agent = agent,
                expected_output="""A JSON list of documents with fields: title, url, snippet, source, date"""
        )
    
    def data_structuring_task(self, agent):
        return Task( 
                name = "data_structuring_task",
                description= "Take raw text from web results and extract structured facts (e.g., pricing info, partnerships, dates, regions). Normalize entities.",
                agent = agent,
                expected_output= "A JSON object with structured data grouped by company and topic"
        )
    
    def impact_analyzer_task(self, agent):
        return Task( 
                name = "impact_analyzer_task",
                description= """Analyze structured and raw extracted intel. Identify tone (positive/negative), and assess strategic impact. Add a short explanation for each impact.
                             Compare competitors, trends, and implications for strategic decision-making.""",
                agent = agent,
                expected_output= "A list of impact summaries with fields: event, sentiment, impact_level, rationale"
        )
    
    def reasoning_and_synthesis_task(self, agent):
        return Task( 
                name = "reasoning_and_synthesis_task",
                description= """Using all prior structured intel, generate an executive-level insight. 
                                Compare competitors, trends, and implications for strategic decision-making.""",
                agent = agent,
                expected_output= "A coherent narrative or summary with clear, actionable insights"
        )
    
    def insight_formatter_task(self, agent):
        return Task( 
                name = "insight_formatter_task",
                description= "Format synthesized insights into a professional report. Use business language, bullets, sections, and optionally Markdown or HTML.",
                agent = agent,
                expected_output= "A polished insight summary, ready to be sent or pasted into a report or deck.",
                output_file = "output/market_research.md"
        )

    
    
