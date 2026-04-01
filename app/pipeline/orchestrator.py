"""
Pipeline orchestrator — coordinates the full audit pipeline.

Called by the gRPC server when job-manager sends an audit request.
Streams status events back as the pipeline progresses.

Flow:
1. Download PDF from R2 (URL provided by job-manager)
2. PageIndex builds document tree
3. Docling extracts text per tree node
4. Build shared context from tree
5. N auditor agents run in parallel
6. Conclusion agent synthesizes findings
7. Return results via gRPC stream
"""

import asyncio
import logging

from app.pipeline.indexer import build_document_tree
from app.pipeline.extractor import extract_text_for_node
from app.pipeline.auditor import run_parallel_auditors
from app.pipeline.conclusion import generate_conclusion

logger = logging.getLogger(__name__)


async def run_pipeline(
    audit_id: str,
    pdf_path: str,
    sop_content: str,
    on_event=None,
) -> dict:
    """Run the full audit pipeline.

    Args:
        audit_id: Unique audit job ID
        pdf_path: Local path to downloaded PDF
        sop_content: SOP text for auditor system prompt
        on_event: Callback to stream events (for gRPC streaming)

    Returns:
        dict with tree, section_results, and conclusion
    """

    async def emit(event_type: str, **kwargs):
        if on_event:
            await on_event(event_type, **kwargs)
        logger.info(f"[{audit_id}] {event_type}: {kwargs.get('message', '')}")

    # 1. Build document tree
    await emit("STATUS_UPDATE", message="Building document tree with PageIndex...")
    tree = await build_document_tree(pdf_path)
    await emit("TREE_BUILT", tree=tree)

    # 2. Extract text per node
    await emit("STATUS_UPDATE", message=f"Extracting text for {len(tree.get('nodes', []))} sections...")
    sections = []
    for node in tree.get("nodes", []):
        text = await extract_text_for_node(
            pdf_path, node.get("start_index", 0), node.get("end_index", 0)
        )
        sections.append({
            "node_id": node.get("node_id"),
            "title": node.get("title"),
            "text": text,
        })

    # 3. Build shared context
    shared_context = _build_shared_context(tree)

    # 4. Run parallel auditors
    await emit("STATUS_UPDATE", message=f"Running {len(sections)} auditor agents in parallel...")
    section_results = await run_parallel_auditors(sections, shared_context, sop_content)

    for result in section_results:
        await emit("SECTION_DONE", section_result=result)

    # 5. Generate conclusion
    await emit("STATUS_UPDATE", message="Generating conclusion...")
    conclusion = await generate_conclusion(section_results)
    await emit("CONCLUSION_DONE", conclusion=conclusion)

    await emit("PIPELINE_DONE", message="Audit complete")

    return {
        "tree": tree,
        "section_results": section_results,
        "conclusion": conclusion,
    }


def _build_shared_context(tree: dict) -> str:
    """Build shared context string from the document tree.

    Extracts key information visible to all auditor agents:
    - Document title/summary from root
    - Section titles and summaries for cross-reference awareness
    """
    parts = [f"Document: {tree.get('title', 'Unknown')}"]

    if tree.get("summary"):
        parts.append(f"Summary: {tree['summary']}")

    parts.append("\nDocument sections:")
    for node in tree.get("nodes", []):
        title = node.get("title", "")
        summary = node.get("summary", "")
        parts.append(f"- {title}: {summary}")

    return "\n".join(parts)
