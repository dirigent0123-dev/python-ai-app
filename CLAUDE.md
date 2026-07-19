# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

# Run with custom port
streamlit run app.py --server.port 8502
```

## Architecture

Single-page Streamlit app where all tool UIs live in `app.py`. Navigation uses a sidebar radio button that sets a `tool` string, and `app.py` branches on that string with `if/elif` blocks — one block per tool. There is no routing library; adding a new tool means adding an entry to the `TOOLS` dict and a new `elif` branch.

All AI logic lives in `tools/`. Each module exports a single function that takes plain Python arguments and returns a string. The functions build a prompt and call `tools/gemini_client.generate()`, which is the only file that touches the Gemini API.

**Gemini client** (`tools/gemini_client.py`): lazy-initializes a module-level singleton `_model` on first call. Model is `gemini-2.0-flash`. API key is read from `.env` via `python-dotenv`. Raises `ValueError` (not a generic exception) when the key is missing or still set to the placeholder — `app.py` catches this separately from other exceptions to show a friendlier message.

**Adding a new tool:**
1. Create `tools/my_tool.py` with a function that accepts parameters and returns `str`
2. Import and call it in `app.py` under a new `elif tool == "my_key":` block
3. Register it in the `TOOLS` dict at the top of `app.py`

## Key conventions

- `show_result()` in `app.py` renders blog output as Markdown (`st.markdown`) and all other tools as a plain `st.text_area`. If a new tool produces Markdown, update the condition inside `show_result`.
- Prompts are entirely in Japanese. Output format instructions are embedded in each prompt (not enforced by post-processing).
- No session state, no database, no authentication — this is a stateless personal tool.
