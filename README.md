---
title: ai astrologist
emoji: ⭐
colorFrom: gray
colorTo: blue
sdk: docker
app_file: app.py
pinned: false
---


[![Build](https://github.com/astro_ai/RAG-LLM/actions/workflows/ci.yml/badge.svg)](https://github.com/TristanHsu/astro_ai/actions)   ← ② GitHub Actions Badge
[![HF Spaces](https://img.shields.io/badge/HF%20Spaces-online-success?logo=huggingface)](https://huggingface.co/spaces/TristanHsu/astro_ai)   ← ③ HF Space Badge

## ✨ Online Demo                ← ④ Demo 區塊標題
https://huggingface.co/spaces/TristanHsu/astro_ai  ← ⑤ Demo 連結

## ⚡ Quick Start (local)        ← ⑥ 本地快速啟動教學
```bash
git clone https://github.com/Tristan-hsu/astro_ai && cd astro_ai
pip install -r requirements.txt
pytest -q
uvicorn api:app --reload
```

[![Test → Build → Deploy to HF Space](https://github.com/Tristan-hsu/astro_ai/actions/workflows/main.yml/badge.svg)](https://github.com/Tristan-hsu/astro_ai/actions/workflows/main.yml)

# Astro Engine & Horoscope – Gradio Edition

A small Gradio app that exposes the same functionality as the original FastAPI
micro-service. Given a date, time and location, it returns the zodiac sign and
J2000 ecliptic longitude for the ten major solar-system bodies.

## Running locally

Install the dependencies and launch the app directly:

```bash
pip install -r requirements.txt
python app.py
```

The interface will be available at <http://127.0.0.1:7860>.

You can also run it from a notebook or Colab:

```python
from app import demo

demo.launch(share=True)
```

## Environment variables (optional)

- `GOOGLE_TZ_API_KEY` – Google Time Zone API key, if available.
- `SWEPH_PATH` – Directory containing Swiss Ephemeris data files.
- `OPENAI_API_KEY` – OpenAI API key for LLM features.

## Dependencies

```
pip install gradio pyswisseph python-dateutil geopy timezonefinder pytz requests
```

## Running with Docker

The repository includes a `dockerfile` so you can run the app without installing
Python locally. Build the image and start the container with:

```bash
docker build -t astro-app -f dockerfile .
docker run -p 7860:7860 astro-app
```

Pass any required environment variables using `-e`, for example:

```bash
docker run -p 7860:7860 \
  -e OPENAI_API_KEY=YOUR_KEY \
  astro-app
```

Once the container starts, open <http://localhost:7860> to use the app.
