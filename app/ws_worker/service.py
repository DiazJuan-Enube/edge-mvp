import json
import logging

logger = logging.getLogger("app.ws_worker.service")

async def handle_message(message: str) -> None:
    try:
        raw_data = json.loads(message)
        
        # Normalización: Convertir siempre a lista
        events = raw_data if isinstance(raw_data, list) else [raw_data]

        for data in events:
            _process_single_event(data)

    except json.JSONDecodeError:
        logger.error("Error: Recibido mensaje que no es JSON válido")
    except Exception as e:
        logger.error(f"Error procesando mensaje: {str(e)}")

def _process_single_event(data: dict):
    event_type = data.get("event_type")
    asset_id = data.get("asset_id")
    
    # Si no hay asset_id, usamos "Global" o intentamos buscarlo en otro lado
    asset_short = asset_id[-8:] if asset_id else "❓"

    if event_type == "book":
        bids = data.get("bids", [])
        asks = data.get("asks", [])
        best_bid = bids[0]['price'] if bids else "-"
        best_ask = asks[0]['price'] if asks else "-"
        logger.info(f"[{asset_short}] 📖 Libro: Compra {best_bid} | Venta {best_ask}")

    elif event_type == "price_change":
        price = data.get("price")
        side = data.get("side")
        
        # --- BLOQUE DE DEPURACIÓN ---
        if price is None:
            # ¡Aquí está el truco! Si llega vacío, imprimimos todo el diccionario
            logger.warning(f"⚠️ Estructura desconocida en price_change: {data}")
        else:
            logger.info(f"[{asset_short}] 💰 Cambio Precio: {price} ({side})")

    elif event_type == "last_trade_price":
        price = data.get("price")
        logger.info(f"[{asset_short}] 🔨 Trade Realizado: {price}")
        
    elif event_type: 
        # Logueamos otros eventos para saber qué son (ej: heartbeat)
        logger.debug(f"Evento informativo: {event_type}")