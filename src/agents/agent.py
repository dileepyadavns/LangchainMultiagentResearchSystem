import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from src.tools.tools import scrap_url, websearch

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0,
    google_api_key=os.getenv("GEMINI_API_KEY"),
)


def search_agent():
    return create_agent(model=llm, tools=[websearch])


def reader_agent():
    return create_agent(
        model=llm,
        tools=[scrap_url],
        system_prompt=(
            "You are a reader agent that extracts content from URLs and answers "
            "questions based on that content. Use the scrap_url tool to extract "
            "content from the provided URLs. If the content is not sufficient to "
            "answer the question, respond with 'Insufficient information to answer "
            "the question.'"
        ),
    )


writer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a writer agent that generates content based on the provided "
            "research. Create a well-structured, informative, factual, and "
            "professional response. If the input is insufficient, say so.",
        ),
        (
            "human",
            "Write a detailed research report on the following topic:\n\n"
            "Topic: {topic}\n"
            "Research gathered: {research}\n\n"
            "Structure the report as:\n"
            "- Introduction\n"
            "- Key Findings\n"
            "- Conclusion\n"
            "- Sources (list all URLs found in the research results)",
        ),
    ]
)

writer_chain = writer_prompt | llm | StrOutputParser()


critic_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a critic agent that evaluates the quality of a research "
            "report. Respond in this exact format:\n"
            "score: (score out of 10)\n"
            "strengths: (list the strengths of the report)\n"
            "areas for improvement: (list the areas where the report can be improved)\n"
            "one line verdict: (provide a one-line verdict on the overall quality)",
        ),
        ("human", "Evaluate the following research report:\n{report}"),
    ]
)

critic_chain = critic_prompt | llm | StrOutputParser()
