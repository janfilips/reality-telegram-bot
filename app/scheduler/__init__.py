# app/scheduler/jobs.py

from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from app.db.crud import upsert_listing
from app.db.models import Listing
from app.filters.listing_filter import GroupRule, match_rule
from app.scrapers.bazos import BazosScraper
from app.telegram.publisher import TelegramPublisher

log = logging.getLogger(__name__)


def build_rules() -> list[GroupRule]:
    # TODO: dať do DB alebo configu. Zatiaľ natvrdo.
    return [
        GroupRule(
            name="BA prenajom",
            district_allow={"BA"},
            listing_type="rent",
            private_only=True,
            telegram_chat_id="-1000000000001",  # TODO: nastav
        ),
        GroupRule(
            name="BA predaj",
            district_allow={"BA"},
            listing_type="sale",
            private_only=True,
            telegram_chat_id="-1000000000002",  # TODO: nastav
        ),
    ]


async def scrape_and_publish(db: Session) -> None:
    publisher = TelegramPublisher()
    rules = build_rules()

    scrapers = [
        BazosScraper(),
        # TODO: RealityScraper(), NehnutelnostiScraper()
    ]

    for scraper in scrapers:
        items = await scraper.fetch()
        for item in items:
            listing = Listing(
                source=item.source,
                external_id=item.external_id,
                url=item.url,
                title=item.title,
                location_text=item.location_text,
                district=item.district,
                listing_type=item.listing_type,
                price_text=item.price_text,
                contact_hint=item.contact_hint,
                is_private=1 if item.is_private else 0,
                raw_json=item.raw_json,
            )

            listing_db, created = upsert_listing(db, listing)
            if not created:
                continue

            for rule in rules:
                if match_rule(listing_db, rule):
                    log.info("Matched rule=%s listing=%s", rule.name, listing_db.url)
                    await publisher.send_listing(rule.telegram_chat_id, listing_db)
