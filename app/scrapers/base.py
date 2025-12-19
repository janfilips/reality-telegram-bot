# app/scrapers/base.py

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NormalizedListing:
    source: str
    external_id: str
    url: str
    title: str
    location_text: str
    district: str
    listing_type: str  # "rent" | "sale"
    price_text: str
    contact_hint: str
    is_private: bool
    raw_json: str
