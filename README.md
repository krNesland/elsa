# elsa
Winternship 2026 onboarding with LLM APIs

For more general knowledge on LLMs, this video bj Andrej Karpathy is recommended: https://www.youtube.com/watch?v=7xTGNNLPyMI

## .env
Make sure to have a .env file in the root of the project with an `OPENAI_API_KEY` set

e.g.
```
OPENAI_API_KEY="your_api_key_here"
```

## Prerequisites
Recommend having homebrew for Mac installations

- `uv`: `brew install uv` on Mac
- `node` `brew install node` on Mac

## Environment
Install: ```uv sync```

## Pre-commit
To check for code issues on commit: ```uv run pre-commit install```

## Cursor / VSCode setting
Settings for auto-format on save is shipped in .vscode
