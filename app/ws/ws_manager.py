from fastapi import WebSocket

class ConnectionManager:
    def __init__(self) -> None:
        self.device_connections: dict[str, WebSocket] = {}
        self.object_connections: dict[str, WebSocket] = {}

    async def connect(self, type: str, id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        if type == "device":
            self.device_connections[id] = websocket
        elif type == "object":
            self.object_connections[id] = websocket

    async def disconnect(self, type: str, id: str, websocket: WebSocket) -> None:
        if type == "device":
            self.device_connections.pop(id)
        elif type == "object":
            self.object_connections.pop(id)

    async def send_to(self, type: str, id: str, massage: dict) -> None:
        ws = None
        if type == "device":
            ws = self.device_connections.get(id, None)
        elif type == "object":
            ws = self.object_connections.get(id, None)

        if ws:
            await ws.send_json(massage)
