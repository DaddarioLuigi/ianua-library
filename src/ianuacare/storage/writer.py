"""Persist pipeline artifacts to database and object storage."""

from __future__ import annotations

from typing import Any

from ianuacare.exceptions.errors import StorageError
from ianuacare.models.context import RequestContext
from ianuacare.models.packet import DataPacket
from ianuacare.storage.bucket import BucketClient
from ianuacare.storage.database import DatabaseClient


class Writer:
    """Writes raw, processed, and result payloads; never logs health data in messages."""

    COL_RAW = "raw_records"
    COL_PROCESSED = "processed_records"
    COL_RESULTS = "inference_results"
    COL_LOGS = "application_logs"

    def __init__(self, db_client: DatabaseClient, bucket_client: BucketClient) -> None:
        self._db = db_client
        self._bucket = bucket_client

    def write_raw(self, packet: DataPacket, context: RequestContext) -> dict[str, Any]:
        """Persist raw payload metadata and optional blob."""
        try:
            key = self._blob_key(context, "raw", packet.metadata)
            blob_ref = self._bucket.upload(key, packet.raw_data)
            record = {
                "user_id": context.user.user_id,
                "product": context.product,
                "blob_key": key,
                "blob": blob_ref,
            }
            return self._db.write(self.COL_RAW, record)
        except Exception as exc:
            raise StorageError("Failed to write raw data") from exc

    def write_processed(self, packet: DataPacket, context: RequestContext) -> dict[str, Any]:
        """Persist processed intermediate data."""
        try:
            key = self._blob_key(context, "processed", packet.metadata)
            blob_ref = self._bucket.upload(key, packet.processed_data)
            record = {
                "user_id": context.user.user_id,
                "product": context.product,
                "blob_key": key,
                "blob": blob_ref,
            }
            return self._db.write(self.COL_PROCESSED, record)
        except Exception as exc:
            raise StorageError("Failed to write processed data") from exc

    def write_result(self, packet: DataPacket, context: RequestContext) -> dict[str, Any]:
        """Persist inference result."""
        try:
            key = self._blob_key(context, "result", packet.metadata)
            blob_ref = self._bucket.upload(key, packet.inference_result)
            record = {
                "user_id": context.user.user_id,
                "product": context.product,
                "blob_key": key,
                "blob": blob_ref,
            }
            return self._db.write(self.COL_RESULTS, record)
        except Exception as exc:
            raise StorageError("Failed to write inference result") from exc

    def write_log(self, message: str, context: RequestContext) -> dict[str, Any]:
        """Persist a non-sensitive log line (no PHI/PII in ``message``)."""
        try:
            record = {
                "user_id": context.user.user_id,
                "product": context.product,
                "message": message,
            }
            return self._db.write(self.COL_LOGS, record)
        except Exception as exc:
            raise StorageError("Failed to write log") from exc

    @staticmethod
    def _blob_key(
        context: RequestContext,
        phase: str,
        packet_meta: dict[str, Any],
    ) -> str:
        """Build a storage key; uses only ids from metadata, not health content."""
        rid = packet_meta.get("request_id", "unknown")
        return f"{context.product}/{context.user.user_id}/{phase}/{rid}"
