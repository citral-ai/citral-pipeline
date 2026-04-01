"""
Auditor agents — parallel LLM calls that audit each document section against SOPs.

Each agent receives: section text + shared context + SOP guidelines.
Every finding MUST cite source text verbatim (anti-hallucination).
Runs N agents concurrently via asyncio.TaskGroup.
"""

import asyncio
import logging

from anthropic import AsyncAnthropic

from app.config import settings

logger = logging.getLogger(__name__)

AUDITOR_SYSTEM_PROMPT = """You are a pharmaceutical compliance auditor reviewing a Batch Manufacturing Record (BMR) section.

## Your task
Audit the provided BMR section against the given SOP/compliance guidelines. For every finding:
1. State the finding clearly
2. Assign severity: CRITICAL / MAJOR / MINOR / INFO
3. Quote the exact source text that supports your finding (verbatim citation)
4. Provide a recommendation

## Rules
- ONLY make findings you can support with direct quotes from the source text
- If you are unsure, say so — do NOT guess or fabricate
- Check for: completeness, accuracy, compliance with SOP, proper documentation
- Consider the shared context for cross-section references

## Output format (JSON)
{
  "findings": [
    {
      "title": "brief finding title",
      "severity": "CRITICAL|MAJOR|MINOR|INFO",
      "description": "detailed description",
      "citation": "exact quoted text from the BMR section",
      "recommendation": "what should be done"
    }
  ],
  "section_summary": "brief compliance assessment of this section",
  "confidence": 0.0-1.0
}
"""


async def audit_section(
    section_text: str,
    shared_context: str,
    sop_content: str,
    node_id: str,
    node_title: str,
) -> dict:
    """Audit a single document section against SOP guidelines."""
    client = AsyncAnthropic(api_key=settings.anthropic_api_key)

    system_prompt = f"{AUDITOR_SYSTEM_PROMPT}\n\n## SOP Guidelines\n{sop_content}\n\n## Shared Context\n{shared_context}"

    response = await client.messages.create(
        model=settings.auditor_model,
        max_tokens=4096,
        temperature=0,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": f"Audit this BMR section:\n\n**Section: {node_title}**\n\n{section_text}",
        }],
    )

    return {
        "node_id": node_id,
        "node_title": node_title,
        "response": response.content[0].text,
        "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
        "model_id": response.model,
    }


async def run_parallel_auditors(
    sections: list[dict],
    shared_context: str,
    sop_content: str,
) -> list[dict]:
    """Run N auditor agents in parallel using asyncio.TaskGroup."""
    semaphore = asyncio.Semaphore(settings.max_concurrent_auditors)

    async def _bounded_audit(section):
        async with semaphore:
            return await audit_section(
                section_text=section["text"],
                shared_context=shared_context,
                sop_content=sop_content,
                node_id=section["node_id"],
                node_title=section["title"],
            )

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(_bounded_audit(s)) for s in sections]

    return [t.result() for t in tasks]
