"""
citral-pipeline — gRPC service for BMR document auditing.

This service receives audit jobs via gRPC, runs the AI pipeline
(PageIndex → Docling → Claude agents → conclusion), and returns results.

It does NOT handle: HTTP, auth, file storage, user management, or SOPs.
Those are handled by other Go services.
"""

import asyncio
import logging

from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def serve():
    """Start the gRPC server."""
    # TODO: set up gRPC server with pipeline service
    # server = grpc.aio.server()
    # pipeline_pb2_grpc.add_PipelineServiceServicer_to_server(PipelineServicer(), server)
    # server.add_insecure_port(f"[::]:{settings.grpc_port}")
    # await server.start()
    # logger.info(f"Pipeline gRPC server started on port {settings.grpc_port}")
    # await server.wait_for_termination()
    logger.info(f"Pipeline service ready (port {settings.grpc_port})")
    logger.info("gRPC server not yet implemented — run pipeline modules directly for testing")


if __name__ == "__main__":
    asyncio.run(serve())
