# app/telegram/publisher.py

import logging

from telegram import Bot

from app.config import settings
from app.db.models import Listing
from app.telegram.templates import format_listing_message

log = logging.getLogger(__name__)


class TelegramPublisher:
    def __init__(self) -> None:
        self._bot = Bot(token=settings.telegram_bot_token) if settings.telegram_bot_token else None

    async def send_listing(self, chat_id: str, listing: Listing) -> None:
        msg = format_listing_message(listing)

        if settings.telegram_dry_run or not self._bot:
            log.info("TELEGRAM DRY RUN -> chat_id=%s\n%s", chat_id, msg)
            return

        await self._bot.send_message(chat_id=chat_id, text=msg, disable_web_page_preview=False)
