from fastapi import WebSocket

class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, device_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections[device_id] = websocket

    def disconnect(self, device_id: str, websocket: WebSocket) -> None:
        self.active_connections.pop(device_id, None)

    async def send_to(self, device_id: str, massage: dict) -> None:
        ws = self.active_connections.get(device_id, None)
        if ws:
            await ws.send_json(massage)
