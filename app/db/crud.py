# app/db/crud.py

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import Listing


def upsert_listing(db: Session, listing: Listing) -> tuple[Listing, bool]:
    """
    Returns: (listing_from_db, created_new)
    """
    stmt = select(Listing).where(Listing.source == listing.source, Listing.external_id == listing.external_id)
    existing = db.execute(stmt).scalar_one_or_none()
    if existing:
        # minimal update - môžeš rozšíriť
        existing.url = listing.url
        existing.title = listing.title
        existing.location_text = listing.location_text
        existing.district = listing.district
        existing.listing_type = listing.listing_type
        existing.price_text = listing.price_text
        existing.contact_hint = listing.contact_hint
        existing.is_private = listing.is_private
        existing.raw_json = listing.raw_json
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing, False

    db.add(listing)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # niekto to už vložil medzičasom
        existing = db.execute(stmt).scalar_one()
        return existing, False

    db.refresh(listing)
    return listing, True
