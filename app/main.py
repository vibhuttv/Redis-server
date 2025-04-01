from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr
import uvicorn
import os
from collections import OrderedDict
import asyncio
from threading import Lock

class LRUCache:
    """Custom implementation of an LRU (Least Recently Used) cache."""

    def __init__(self, capacity: int = 10000):
        """Initialize the LRU cache with a given capacity."""
        self.capacity = capacity
        self.cache = OrderedDict()  
        self.lock = Lock()  

    def put(self, key: str, value: str):
        """Insert a key-value pair into the cache."""
        if len(key) > 256 or len(value) > 256:
            raise ValueError("Key or value exceeds 256 characters")

        with self.lock:
            if key in self.cache:
                self.cache.pop(key)
            
            self.cache[key] = value

            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)  

    def get(self, key: str):
        """Retrieve a value from the cache; return None if not found."""
        with self.lock:
            if key not in self.cache:
                return None  
            
            value = self.cache.pop(key)
            self.cache[key] = value
            return value

app = FastAPI()

max_size = int(os.getenv("MAX_CACHE_SIZE", 10000))
cache = LRUCache(capacity=max_size)

class CacheEntry(BaseModel):
    key: constr(max_length=256)
    value: constr(max_length=256)

@app.post("/put")
async def put_key(entry: CacheEntry):
    """Store a key-value pair in the cache."""
    try:
        await asyncio.to_thread(cache.put, entry.key, entry.value)
        return {"status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get/")
async def get_key(key: str):
    """Retrieve a value from the cache by key."""
    value = await asyncio.to_thread(cache.get, key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"value": value}

@app.get("/health")
async def health_check():
    """Health check endpoint to verify service status."""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7171, workers=4)

