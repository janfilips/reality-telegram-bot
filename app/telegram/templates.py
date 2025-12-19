# app/telegram/templates.py

from app.db.models import Listing


def format_listing_message(listing: Listing) -> str:
    parts: list[str] = []
    if listing.title:
        parts.append(listing.title.strip())

    meta = []
    if listing.location_text:
        meta.append(listing.location_text.strip())
    if listing.price_text:
        meta.append(listing.price_text.strip())
    if meta:
        parts.append(" - ".join(meta))

    parts.append(listing.url)
    return "\n".join(parts).strip()
