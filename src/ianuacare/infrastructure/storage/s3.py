"""S3 object storage adapter."""

from __future__ import annotations

import json
from typing import Any

try:  # Optional dependency
    import boto3
except Exception:  # pragma: no cover - import-time optional dependency handling
    boto3 = None  # type: ignore[assignment]


class S3BucketClient:
    """Store and retrieve payloads in an S3 bucket."""

    def __init__(self, bucket_name: str, region: str | None = None) -> None:
        if boto3 is None:
            raise ImportError("S3BucketClient requires boto3")
        self._bucket_name = bucket_name
        self._s3 = boto3.client("s3", region_name=region)

    def upload(self, key: str, content: Any) -> dict[str, Any]:
        body = content if isinstance(content, (bytes, bytearray)) else json.dumps(content).encode()
        self._s3.put_object(Bucket=self._bucket_name, Key=key, Body=body)
        return {"ok": True, "key": key, "bucket": self._bucket_name}

    def download(self, key: str) -> Any:
        response = self._s3.get_object(Bucket=self._bucket_name, Key=key)
        return response["Body"].read()
