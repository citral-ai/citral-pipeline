"""
Conclusion agent — synthesizes all section audit reports into a final assessment.

Produces: confidence index, chain-of-thought summary, aggregated findings, suggestions.
"""

from anthropic import AsyncAnthropic

from app.config import settings

CONCLUSION_SYSTEM_PROMPT = """You are a senior pharmaceutical compliance auditor. You are reviewing the combined audit findings from multiple sections of a Batch Manufacturing Record (BMR).

## Your task
Synthesize all section-level findings into a unified audit conclusion.

## Output format (JSON)
{
  "confidence_index": 0-100,
  "overall_assessment": "PASS / CONDITIONAL_PASS / FAIL",
  "chain_of_thought": {
    "correct": ["list of things that meet compliance"],
    "issues": ["list of compliance issues found"],
    "improvements": ["list of things that could be better"]
  },
  "critical_findings": ["list of critical/major findings requiring immediate attention"],
  "suggestions": ["actionable recommendations"],
  "flag_summary": {
    "critical": 0,
    "major": 0,
    "minor": 0,
    "info": 0
  }
}

## Rules
- Weigh findings by severity — one CRITICAL finding can override many MINOR passes
- Resolve conflicting signals across sections
- Be conservative — when in doubt, flag for human review
- This is a decision-support tool, NOT a final compliance determination
"""


async def generate_conclusion(audit_results: list[dict]) -> dict:
    """Synthesize all auditor reports into a final conclusion."""
    client = AsyncAnthropic(api_key=settings.anthropic_api_key)

    # Compile all section results into one prompt
    sections_summary = []
    for result in audit_results:
        sections_summary.append(
            f"### Section: {result['node_title']}\n{result['response']}"
        )

    all_findings = "\n\n".join(sections_summary)

    response = await client.messages.create(
        model=settings.conclusion_model,
        max_tokens=4096,
        temperature=0,
        system=CONCLUSION_SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Synthesize these section audit reports into a final conclusion:\n\n{all_findings}",
        }],
    )

    return {
        "response": response.content[0].text,
        "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
        "model_id": response.model,
    }
