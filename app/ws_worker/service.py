import logging

logger = logging.getLogger("app.ws_worker.service")


async def handle_message(message: str) -> None:
    """Simple handler: imprimir el mensaje tal cual y registrar una línea.

    No se realiza parseo ni persistencia aquí; sólo salida por consola para depuración.
    """
    try:
        # Print to stdout for immediate visibility
        print(message)
    except Exception:
        # Silently ignore printing errors but still log
        logger.exception("Failed to print message")

    logger.info("Received message (raw)")