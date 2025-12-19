# app/ws_worker/schemas.py

# URL del CLOB de Polymarket
POLYMARKET_WS_URL = "wss://ws-subscriptions-clob.polymarket.com/ws/market"

# ID DEL ACTIVO (Asset ID)
# IMPORTANTE: Reemplaza este ID con el que quieras monitorear.
# Este ejemplo es para un mercado activo (Trump vs Harris o similar para testing).
TARGET_ASSET_ID = "11862165566757345985240476164489718219056735011698825377388402888080786399275"

# Definimos el payload de suscripción aquí para mantener limpio el bootstrap
SUBSCRIPTION_PAYLOAD = {
    "assets_ids": [TARGET_ASSET_ID],
    "type": "market"
}