from src.llm.ollama_llm import OllamaLLM
from datetime import datetime
from src.utils.logging import info

# Escape braces {{ }} so .format() doesn't treat them as placeholders
PROMPT_TMPL = """
You are a research assistant. Given a user query and a set of retrieved text passages with metadata,
write a concise, structured research report.

Return BOTH:
1️⃣ A JSON summary with the following schema:
{{
  "query": str,
  "date_utc": str,
  "key_findings": [str],
  "evidence": [
     {{"title": str, "url": str, "published": str | null, "support": str}}
  ],
  "limitations": [str]
}}
2️⃣ A Markdown summary for human readability.

Guidelines:
- Prefer recent, relevant sources.
- Cite titles and URLs.
- Be concise and factual.
- Avoid speculation.

User Query:
"{query}"

Retrieved Passages:
{passages}

Now produce the JSON block first, then the Markdown summary.
"""


class SummarizerAgent:
    """Summarizes retrieved papers into structured JSON + Markdown reports."""

    def __init__(self, model: str | None = None):
        self.llm = OllamaLLM(model)

    def summarize(self, query: str, retrieved):
        info("Generating summary report with Ollama LLM...")

        # Build readable passage block
        blocks = []
        for docs, metas in zip(retrieved.get("documents", [[]]), retrieved.get("metadatas", [[]])):
            for d, m in zip(docs, metas):
                title = (m or {}).get("title")
                url = (m or {}).get("url")
                published = (m or {}).get("published")
                snippet = d[:1000].replace("\n", " ")
                blocks.append(f"TITLE: {title}\nURL: {url}\nPUBLISHED: {published}\nPASSAGE: {snippet}\n---")

        passages = "\n".join(blocks[:10])
        prompt = PROMPT_TMPL.format(query=query, passages=passages)

        result = self.llm.generate(prompt)
        return result
