from collections.abc import Callable

from src.agents.agent import (
    critic_chain,
    reader_agent,
    search_agent,
    writer_chain,
)

def reasearch_pipeline(
    topic: str,
    progress_callback: Callable[[str], None] | None = None,
    step_callback: Callable[[str, str], None] | None = None,
) -> dict:
   state = {}
   state["topic"] = topic

   if progress_callback:
       progress_callback("Searching the web")
   print("\n"+"="*50)
   print("step1: Researching the topic using search agent")
   print("="*50+"\n")
   search_agent_instance = search_agent()
   search_results = search_agent_instance.invoke(
       {"messages": [("user", f"Find recent information on {topic}")]}
   )
   state["search_results"] = search_results
   search_result_text = search_results["messages"][-1].content
   if step_callback:
       step_callback("Web search", search_result_text)
   print(f"Search Results:\n{search_results}\n")


   if progress_callback:
       progress_callback("Reading relevant pages")
   print("\n"+"="*50)
   print("step2: Extracting content from search results using reader agent")   
   reader_agent_instance = reader_agent()
   reader_agent_results = reader_agent_instance.invoke(
       {
           "messages": [
               (
                   "user",
                   f"Research topic: {topic}\n"
                   "Extract content from the most relevant URLs in these search results:\n"
                   f"{search_result_text[:8000]}",
               )
           ]
       }
   )

   state["scraped_content"] = reader_agent_results["messages"][-1].content
   if step_callback:
       step_callback("Read relevant pages", state["scraped_content"])
   print(f"Scraped Content:\n{state['scraped_content']}\n")


   if progress_callback:
       progress_callback("Writing the research report")
   print("\n"+"="*50)
   print("step3: Generating research report using writer chain")

   research_combined=f"search_results: {state['search_results']}\n\nscraped_content: {state['scraped_content']}"

   state["research_report"] = writer_chain.invoke({"topic": topic, "research": research_combined})
   if step_callback:
       step_callback("Write report", state["research_report"])
   print(f"Research Report:\n{state['research_report']}\n")

   if progress_callback:
       progress_callback("Reviewing the report")
   print("\n"+"="*50)
   print("step4: Evaluating research report using critic chain")
   state["report_evaluation"] = critic_chain.invoke(
       {"report": state["research_report"]}
   )
   if step_callback:
       step_callback("Review report", state["report_evaluation"])
   print(f"Report Evaluation:\n{state['report_evaluation']}\n")
   return state