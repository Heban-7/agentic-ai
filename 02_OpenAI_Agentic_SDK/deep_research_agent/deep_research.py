import asyncio
import gradio as gr
from dotenv import load_dotenv

from research_manager import ResearchManager

load_dotenv(override=True)


CUSTOM_CSS = """
footer {
    visibility: hidden;
}

.gradio-container {
    max-width: 1400px !important;
    margin: auto;
}

#title {
    text-align: center;
    margin-bottom: 10px;
}

#subtitle {
    text-align: center;
    margin-bottom: 30px;
    color: gray;
}

.status-box {
    border-radius: 12px;
    padding: 12px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
}
"""


async def run_research(query: str):
    """Run deep research pipeline and stream updates"""

    if not query.strip():
        yield (
            "❌ Please enter a research topic.",
            ""
        )
        return

    status_updates = []
    final_report = ""

    async for chunk in ResearchManager().run(query):

        if chunk.startswith("#") or len(chunk) > 500:
            final_report = chunk
        else:
            status_updates.append(f"- {chunk}")

        yield (
            "\n".join(status_updates),
            final_report
        )


with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="sky",
        secondary_hue="blue",
        neutral_hue="slate"
    ),
    css=CUSTOM_CSS,
    title="Deep Research Agent"
) as ui:

    gr.Markdown(
        """
        # 🔬 Deep Research AI Agent
        """,
        elem_id="title"
    )

    gr.Markdown(
        """
        Multi-agent AI system that:
        plans research → searches web → synthesizes findings → writes reports → sends email
        """,
        elem_id="subtitle"
    )

    with gr.Row():

        with gr.Column(scale=1):

            gr.Markdown("## ⚙️ Research Input")

            query_input = gr.Textbox(
                label="Research Topic",
                placeholder="Example: Future of AI startups in Africa",
                lines=5
            )

            run_button = gr.Button(
                "🚀 Start Deep Research",
                variant="primary",
                size="lg"
            )

            clear_button = gr.Button(
                "🧹 Clear",
                variant="secondary"
            )

            gr.Examples(
                examples=[
                    ["Future of AI in healthcare"],
                    ["Impact of quantum computing on cybersecurity"],
                    ["Top startup opportunities in Ethiopia"],
                    ["Future of renewable energy in Africa"],
                ],
                inputs=query_input,
            )

            with gr.Accordion("ℹ️ How This Works", open=False):
                gr.Markdown(
                    """
                    This system uses multiple AI agents:

                    1. **Planner Agent** → Generates search strategy
                    2. **Search Agent** → Searches the web
                    3. **Writer Agent** → Synthesizes full report
                    4. **Email Agent** → Sends formatted email

                    Features:
                    - Parallel web research
                    - AI synthesis
                    - Long-form report generation
                    - Async execution
                    - Streaming updates
                    """
                )

        with gr.Column(scale=2):

            gr.Markdown("## 📡 Research Progress")

            status_output = gr.Markdown(
                value="Waiting to start research...",
                elem_classes=["status-box"]
            )

            gr.Markdown("## 📄 Final Research Report")

            report_output = gr.Markdown()

    run_button.click(
        fn=run_research,
        inputs=query_input,
        outputs=[status_output, report_output]
    )

    query_input.submit(
        fn=run_research,
        inputs=query_input,
        outputs=[status_output, report_output]
    )

    clear_button.click(
        lambda: (
            "Waiting to start research...",
            "",
            ""
        ),
        outputs=[status_output, report_output, query_input]
    )


ui.queue()
ui.launch(inbrowser=True)
