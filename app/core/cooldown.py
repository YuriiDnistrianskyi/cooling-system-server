import asyncio, time

from app.core.config import COOLDOWN

last_command_ts = {}
lock = asyncio.Lock()

async def can_send_command(object_id: int) -> bool:
    async with lock:
        now = time.time()
        last_ts = last_command_ts.get(object_id, 0)

        if now - last_ts >= COOLDOWN:
            last_command_ts[object_id] = now
            return True

        return False
