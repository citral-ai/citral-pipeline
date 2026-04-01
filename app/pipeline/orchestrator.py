"""
Pipeline orchestrator — coordinates the full audit pipeline.

Flow:
1. PageIndex builds document tree (indexer.py)
2. Docling extracts text per tree node (extractor.py)
3. Shared context built from tree root + key sections
4. N auditor agents run in parallel (auditor.py)
5. Conclusion agent synthesizes findings (conclusion.py)
6. Report generated (reporter.py)
"""


async def run_pipeline(audit_id: str) -> None:
    """Run the full audit pipeline for a given audit job."""
    # TODO: implement pipeline orchestration
    # 1. Update status: indexing
    # 2. Build PageIndex tree
    # 3. Update status: extracting
    # 4. Extract text per node
    # 5. Build shared context
    # 6. Update status: auditing
    # 7. Run parallel auditor agents
    # 8. Update status: concluding
    # 9. Run conclusion agent
    # 10. Update status: reporting
    # 11. Generate report
    # 12. Update status: done
    pass
