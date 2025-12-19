# app/ws_worker/bootstrap.py
import asyncio
import logging
import signal
import sys

# Ajusta los imports según cómo ejecutes tu proyecto (como módulo o script)
from app.ws_worker.consumer import WebsocketConsumer
from app.ws_worker.service import handle_message
from app.ws_worker.schemas import POLYMARKET_WS_URL, SUBSCRIPTION_PAYLOAD

# Configuración de logs para ver la salida en consola
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("app.ws_worker.bootstrap")

async def main() -> None:
    """
    Función principal para arrancar el monitor de Polymarket.
    """
    logger.info("🚀 Iniciando Worker de Polymarket...")

    # 1. Instanciar el Consumer
    # Le pasamos la URL, la función que procesa los datos y el payload de suscripción
    consumer = WebsocketConsumer(
        url=POLYMARKET_WS_URL,
        on_message=handle_message,       # La lógica de service.py
        subscribe_payload=SUBSCRIPTION_PAYLOAD  # La config de schemas.py
    )

    # 2. Configurar el apagado elegante (Graceful Shutdown)
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def _signal_handler(*args):
        logger.info("🛑 Señal de parada recibida. Cerrando conexiones...")
        consumer.stop() # Método .stop() de tu clase Consumer
        stop_event.set()

    # Capturar CTRL+C (SIGINT) y SIGTERM
    try:
        loop.add_signal_handler(signal.SIGINT, _signal_handler)
        loop.add_signal_handler(signal.SIGTERM, _signal_handler)
    except NotImplementedError:
        # Windows a veces da problemas con signal handlers en ciertos loops
        logger.warning("Signal handlers no soportados en este entorno (probablemente Windows).")

    # 3. Ejecutar el consumidor en una tarea de fondo
    consumer_task = asyncio.create_task(consumer.start())
    
    logger.info(f"Suscrito al Asset ID: {SUBSCRIPTION_PAYLOAD['assets_ids'][0][:10]}...")

    # 4. Esperar hasta que se indique parar
    await stop_event.wait()

    # 5. Limpieza
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        pass
    
    logger.info("Worker finalizado correctamente.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Fallback por si el signal handler no captura el primer CTRL+C
        pass