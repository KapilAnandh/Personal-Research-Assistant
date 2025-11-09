
---

## 📄 `models/llm.md`

```markdown
# 🧠 Local LLM — `gemma3:270m`

## Overview
The Research Assistant uses **Gemma 3 (270 M)** from Google via **Ollama** as its
local summarization and reasoning model.

- **Model**: `gemma3:270m`
- **Provider**: [Ollama](https://ollama.com/library/gemma3)
- **Size**: ~291 MB
- **License**: Open, commercial-use allowed
- **Inference**: Fully local CPU/GPU execution
- **Purpose**: Structured summarization, synthesis, concise reasoning

---

## Why `gemma3:270m`
| Feature | Description |
|----------|-------------|
| 🧩 Lightweight | Runs on standard laptops (4 GB+ RAM). |
| 🔒 Private | No internet calls; inference happens via local Ollama. |
| ⚡ Fast | Ideal for summarizing 5–10 research papers at once. |
| 🧠 Extensible | You can swap to `llama3.2:3b`, `phi3:mini`, etc. by editing `.env`. |

---

## Prompt Design
The model is prompted with structured templates (see `summarizer.py`):

```text
You are a research assistant. Given retrieved passages...
→ produce JSON with key findings, evidence, limitations
→ then generate readable Markdown summary.
