import time
import logging
from typing import Any, List, Union
from src.domain.enums import JobSource
from src.ingestion.base import BaseScraper
from src.ingestion.clients.remoteok import RemoteOKClient
from src.ingestion.parsers.remoteok import RemoteOKParser

logger = logging.getLogger("jobpulse_ai.scrapers.remoteok")

class RemoteOKScraper(BaseScraper):
    def __init__(self):
        self._client = RemoteOKClient()
        self._parser = RemoteOKParser()

    @property
    def source_name(self) -> str:
        return JobSource.REMOTEOK.value

    @property
    def parser(self) -> RemoteOKParser:
        return self._parser

    def fetch(self) -> Union[bytes, dict, str, List[Any]]:
        logger.info("[REMOTEOK] Fetch started")
        data = self._client.fetch_jobs()
        logger.info("[REMOTEOK] Response received (200)")
        logger.info(f"[REMOTEOK] Records received: {len(data)}")
        return data
