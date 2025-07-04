from __future__ import annotations

import datetime as dt

import gradio as gr

from astro_computation import astro_data
from llm import generate_responses, summurize


def summarize_astrology(
    datetime_str: str,
    location: str,
    provider: str,
    api_key: str,
    model_id: str,
) -> str:
    """Generate a Chinese horoscope summary for the given parameters."""
    try:
        docs = astro_data(datetime_str, location)
        responses = generate_responses(docs, provider, model_id, api_key)
        return summurize(responses, provider, model_id, api_key)
    except Exception as exc:
        return f"Error: {exc}"


demo = gr.Interface(
    summarize_astrology,
    [
        gr.Textbox(
            label="Date & Time (ISO‑8601)",
            value=dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        ),
        gr.Textbox(label="Location", value="Taipei"),
        gr.Dropdown(
            [ "openai"],
            label="請選擇一個選項",
        ),
        gr.Textbox(label="API-key", type="password", placeholder="API-key"),
        gr.Textbox(label="Model", value="gpt-4o-mini"),
    ],
    gr.Textbox(label="Ephemeris"),
    title="Horoscope Astro Engine",
    description="<br><br> 請輸入以下資訊，就可以算出關於你出生的星座描述！",
    submit_btn="Calculate",
)


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
