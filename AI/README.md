# AI — LangChain experiments

Sandbox for learning and prototyping with LangChain, LangGraph, and various LLM providers.

## Stack

- Python 3.14, managed by [`uv`](https://docs.astral.sh/uv/)
- `langchain` + provider SDKs (OpenAI, Anthropic, Google, Groq, HuggingFace, Cohere, DeepSeek)
- `pydantic-settings` for typed configuration loaded from `.env`
- Jupyter for notebook-driven exploration

## Layout

```
AI/
├── config/              # Typed Settings (pydantic-settings) loaded from .env
├── langchain/           # LangChain notebooks (1.intro.ipynb, ...)
├── langgraph/           # LangGraph experiments
├── notebooks/           # Free-form scratch notebooks
├── .env                 # Local secrets (git-ignored)
├── pyproject.toml       # Dependencies + project metadata
└── uv.lock              # Locked dependency graph
```

## Setup

```bash
cd AI
uv sync
```

Create `.env` (see `config/environment.py` for the full list of supported keys):

```env
APP_ENV=development
APP_DEBUG=true

OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...
# ...other provider keys as needed

LANGSMITH_API_KEY=lsv2_...
LANGSMITH_TRACING=false
LANGSMITH_PROJECT=default
```

## Running notebooks

Open any notebook under `AI/langchain/` and select the `AI/.venv` interpreter as the kernel. The first cell of each tutorial verifies the environment.

## Adding dependencies

```bash
uv add <package>
```

## Conventions

- Field names in `Settings` are namespaced (`APP_DEBUG`, not `DEBUG`) to avoid collisions with shell-level environment variables.
- API keys are typed as `SecretStr`; access raw values with `.get_secret_value()`.
- `from config import settings` at the top of any module loads `.env` once and exports keys to `os.environ` for third-party SDKs.
