# app/filters/listing_filter.py

from __future__ import annotations

from dataclasses import dataclass

from app.db.models import Listing


@dataclass(frozen=True)
class GroupRule:
    name: str
    district_allow: set[str]
    listing_type: str  # "rent" | "sale"
    private_only: bool
    telegram_chat_id: str


def match_rule(listing: Listing, rule: GroupRule) -> bool:
    if rule.listing_type and listing.listing_type != rule.listing_type:
        return False

    if rule.district_allow and listing.district not in rule.district_allow:
        return False

    if rule.private_only and listing.is_private != 1:
        return False

    return True
