# app/scrapers/bazos.py

from __future__ import annotations

import json
import logging
from typing import List

import httpx

from app.scrapers.base import NormalizedListing

log = logging.getLogger(__name__)


class BazosScraper:
    source = "bazos"

    async def fetch(self) -> List[NormalizedListing]:
        # XXX TODO: reálne endpointy/HTML parsing
        # Zatiaľ len fake dáta aby pipeline fungovala.
        log.info("Scraping bazos (stub)")
        await httpx.AsyncClient().aclose()

        return [
            NormalizedListing(
                source=self.source,
                external_id="stub-1",
                url="https://example.com/listing/1",
                title="2i byt - Ružinov",
                location_text="Bratislava - Ružinov",
                district="BA",
                listing_type="rent",
                price_text="750 EUR",
                contact_hint="owner",
                is_private=True,
                raw_json=json.dumps({"stub": True}),
            )
        ]
