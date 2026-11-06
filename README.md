# Multi-agent Research System

## Run the Streamlit app

Install the project dependencies, then add these API keys to a `.env` file in
the project directory:

```text
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Start the app from this directory:

```bash
streamlit run app.py
```

Enter a research topic and select **Research**. The app displays the generated
report and evaluation, with the search results and extracted page content
available in expandable sections. You can also download the report as Markdown.
