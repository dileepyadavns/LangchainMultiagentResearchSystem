import streamlit as st

from src.pipeline.pipeline import reasearch_pipeline


st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔎",
    layout="wide",
)

st.title("AI Research Assistant")
st.write(
    "Enter a topic to search the web, read relevant pages, write a report, "
    "and review the result."
)

with st.form("research_form"):
    topic = st.text_input(
        "Research topic",
        placeholder="For example: The impact of AI on healthcare",
    )
    submitted = st.form_submit_button("Research", type="primary")

if submitted:
    if not topic.strip():
        st.warning("Enter a topic before starting the research.")
    else:
        step_titles = [
            "Web search",
            "Read relevant pages",
            "Write report",
            "Review report",
        ]
        step_placeholders = []
        try:
            st.subheader("Pipeline progress")
            for index, title in enumerate(step_titles, start=1):
                step_placeholders.append(st.empty())
                step_placeholders[-1].info(f"Step {index}: Waiting — {title}")

            def update_step(message):
                index = step_titles.index(message) + 1
                step_placeholders[index - 1].info(
                    f"Step {index}: In progress — {message}"
                )

            def show_step_output(title, content):
                index = step_titles.index(title) + 1
                with step_placeholders[index - 1].container():
                    with st.expander(f"Step {index}: {title} — complete", expanded=True):
                        st.markdown(content)

            with st.status("Starting research...", expanded=True) as status:
                progress_titles = {
                    "Searching the web": "Web search",
                    "Reading relevant pages": "Read relevant pages",
                    "Writing the research report": "Write report",
                    "Reviewing the report": "Review report",
                }

                def update_progress(message):
                    status.update(label=message)
                    update_step(progress_titles[message])

                result = reasearch_pipeline(
                    topic.strip(),
                    progress_callback=update_progress,
                    step_callback=show_step_output,
                )
                status.update(label="Research complete", state="complete")
            st.session_state["research_result"] = result
        except Exception as exc:
            st.error("The research workflow failed.")
            st.exception(exc)

result = st.session_state.get("research_result")
if result:
    st.header(f"Research: {result['topic']}")

    st.subheader("Research report")
    st.markdown(result["research_report"])
    st.download_button(
        "Download report",
        data=result["research_report"],
        file_name="research-report.md",
        mime="text/markdown",
    )

    st.subheader("Report evaluation")
    st.markdown(result["report_evaluation"])

    with st.expander("Search results"):
        messages = result["search_results"].get("messages", [])
        if messages:
            st.markdown(messages[-1].content)
        else:
            st.write(result["search_results"])

    with st.expander("Extracted page content"):
        st.markdown(result["scraped_content"])