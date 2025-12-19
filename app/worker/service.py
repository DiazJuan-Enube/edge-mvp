import json
import logging
from typing import Any

from app.db.session import AsyncSessionLocal
from app.db.models import Trade

logger = logging.getLogger("app.worker.service")


async def handle_message(raw_msg: str) -> None:
    """Parse a message and persist a Trade example to the DB.

    This is a simple example showing how to use `AsyncSessionLocal`.
    Adapt to your message schema and repository functions.
    """
    try:
        data = json.loads(raw_msg)
    except Exception:
        logger.exception("Invalid JSON message")
        return

    # expected minimal fields for a Trade
    condition_id = data.get("condition_id")
    proxy_wallet = data.get("proxy_wallet")
    timestamp = data.get("timestamp")

    if not (condition_id and proxy_wallet and timestamp):
        logger.warning("Skipping message: missing required trade fields")
        return

    # build Trade model with known fields; adapt as needed
    trade = Trade(
        condition_id=condition_id,
        proxy_wallet=proxy_wallet,
        timestamp=int(timestamp),
        transaction_hash=data.get("transaction_hash"),
        side=data.get("side"),
        asset=data.get("asset"),
        outcome=data.get("outcome"),
        outcome_index=data.get("outcome_index"),
        price=data.get("price"),
        size=data.get("size"),
        title=data.get("title"),
        slug=data.get("slug"),
        event_slug=data.get("event_slug"),
        icon=data.get("icon"),
        raw_json=data,
    )

    async with AsyncSessionLocal() as session:
        session.add(trade)
        try:
            await session.commit()
            logger.debug("Trade persisted: %s", getattr(trade, "trade_id", None))
        except Exception:
            logger.exception("Failed to persist trade; rolling back")
            await session.rollback()
