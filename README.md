# SkyRecoverAI

Agentic AI portfolio project for airline disruption recovery using Python, Streamlit, and LangGraph.

## Tech Stack
- Python 3.11+
- Streamlit
- LangGraph
- OpenAI API

## Project Layout
- [agents](agents/README.md)
- [workflows](workflows/README.md)
- [services](services/README.md)
- [data](data/README.md)
- [docs](docs/README.md)
- [tests](tests/README.md)

## Quick Start
1. Create and activate a virtual environment.
	- Windows PowerShell:
	  - py -m venv .venv
	  - .\.venv\Scripts\Activate.ps1
	- macOS/Linux:
	  - python3 -m venv .venvcd scripts
	  - source .venv/bin/activate

2. Install dependencies.
	- python -m pip install -r requirements.txt

3. Configure environment variables.
	- Copy .env.example to .env
	- Set OPENAI_API_KEY in .env
	- Optional: set OPENAI_MODEL (default is gpt-4o-mini)

4. Run the Streamlit app.
	- Preferred (works even if streamlit is not on PATH):
	  - python -m streamlit run streamlit_app.py

5. Open the app in your browser.
	- http://localhost:8501

## Optional Validation
1. Run a workflow smoke test.
	- python -m pytest tests/test_workflow_smoke.py

2. Execute one simulation in UI and verify output.
	- data/output/cases_output.json should be created or updated.

## Troubleshooting
- If streamlit command is not found, use:
  - python -m streamlit run streamlit_app.py
- If OpenAI calls fail, verify OPENAI_API_KEY is set in your active environment.

## Architecture
- [MVP Architecture](docs/architecture.md)
- [Repository Structure Guide](docs/repository-structure.md)
