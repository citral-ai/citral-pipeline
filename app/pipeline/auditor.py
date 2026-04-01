"""
Auditor agents — parallel LLM calls that audit each document section against SOPs.

Each agent receives: section text + shared context + SOP guidelines.
Each agent must cite source text for every finding.
"""


async def audit_section(
    section_text: str,
    shared_context: str,
    sop_content: str,
    node_title: str,
) -> dict:
    """Audit a single document section against SOP guidelines.

    Returns structured findings with citations.
    """
    # TODO: implement with Anthropic async SDK
    # from anthropic import AsyncAnthropic
    # client = AsyncAnthropic()
    # response = await client.messages.create(
    #     model="claude-sonnet-4-20250514",
    #     max_tokens=4096,
    #     system=f"{sop_content}\n\nShared context:\n{shared_context}",
    #     messages=[{"role": "user", "content": f"Audit this BMR section:\n\n{section_text}"}],
    # )
    # return parse_findings(response)
    pass


async def run_parallel_auditors(
    sections: list[dict],
    shared_context: str,
    sop_content: str,
) -> list[dict]:
    """Run N auditor agents in parallel using asyncio.TaskGroup."""
    # TODO: implement with asyncio.TaskGroup
    # async with asyncio.TaskGroup() as tg:
    #     tasks = [
    #         tg.create_task(audit_section(s["text"], shared_context, sop_content, s["title"]))
    #         for s in sections
    #     ]
    # return [t.result() for t in tasks]
    pass
