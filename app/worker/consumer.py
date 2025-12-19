import asyncio
import logging
from typing import Callable

import websockets

from app.worker.service import handle_message

logger = logging.getLogger("app.worker.consumer")


class WebsocketConsumer:
    def __init__(self, url: str, on_message: Callable = handle_message):
        self.url = url
        self.on_message = on_message
        self._stopped = False

    async def _consume(self, ws: websockets.WebSocketClientProtocol):
        async for msg in ws:
            try:
                await self.on_message(msg)
            except Exception:
                logger.exception("Error handling message")

    async def start(self):
        backoff = 1
        while not self._stopped:
            try:
                async with websockets.connect(self.url) as ws:
                    logger.info("Connected to websocket %s", self.url)
                    backoff = 1
                    await self._consume(ws)
            except Exception as exc:
                logger.exception("WS connection error: %s", exc)
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 30)

    def stop(self):
        self._stopped = True
