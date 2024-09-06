import json
from typing import Any
from unittest.mock import AsyncMock

class AsyncRedisMock:
    def __init__(self):
        self.store = {}

    async def setex(self, key: str, expire: int, value: Any):
        self.store[key] = value

    async def get(self, key: str):
        return self.store.get(key)

    async def delete(self, key: str):
        if key in self.store:
            del self.store[key]

# Use o AsyncMock para simular o comportamento assíncrono do Redis
async_redis_mock = AsyncRedisMock()
