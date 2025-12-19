import asyncio
import logging
import os
import signal

from app.worker.consumer import WebsocketConsumer

logger = logging.getLogger("app.worker")


def _setup_logging():
    level = os.environ.get("LOG_LEVEL", "INFO")
    logging.basicConfig(level=level)


async def _run_consumer(url: str) -> None:
    consumer = WebsocketConsumer(url)
    await consumer.start()


async def main() -> None:
    _setup_logging()
    ws_url = os.environ.get("WS_URL")
    if not ws_url:
        logger.error("WS_URL not set. Exiting.")
        return

    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def _signal(_sig, _frame):
        logger.info("Received stop signal")
        stop_event.set()

    loop.add_signal_handler(signal.SIGINT, lambda: _signal(None, None))
    loop.add_signal_handler(signal.SIGTERM, lambda: _signal(None, None))

    # run consumer in a task; stop_event will be used to gracefully exit
    task = asyncio.create_task(_run_consumer(ws_url))
    await stop_event.wait()
    logger.info("Shutting down worker")
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        logger.info("Consumer task cancelled")


if __name__ == "__main__":
    asyncio.run(main())
