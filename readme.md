# FastAPI-Based Key-Value Cache Service

This project is a lightweight key-value caching service built using **FastAPI**. It supports storing and retrieving data with an in-memory LRU (Least Recently Used) cache and allows for configurable cache sizing.

## Core Features

- **Server Health Endpoint**: Verify if the service is operational.
- **Add Key-Value Pairs**: Save key-value entries to the cache.
- **Fetch by Key**: Retrieve stored values using a specific key.
- **Configurable Cache Limit**: Define the maximum cache size through an environment variable (`MAX_CACHE_SIZE`).

## Requirements

To run this service, you'll need Python version 3.7 or above, along with these dependencies:

- FastAPI
- uvicorn
- cachetools
- pydantic

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/vibhuttv/Redis-server.git
cd redis-server
```

### 2. Pull and Run the Docker Container

```bash
docker pull vibhuk2003/redis-key-value-server
```

## Launching the Server

Start the service using Docker Compose:

```bash
docker compose up
```

The server will become accessible at `http://127.0.0.1:7171`.

To define a custom cache limit, set the `MAX_CACHE_SIZE` environment variable (value in bytes):

```bash
export MAX_CACHE_SIZE=$((10 * 1024 * 1024))  # Sets cache size to 10 MB
```

By default, the cache will use 70% of 2GB (approximately 1.4GB).

## API Overview

### **POST `/put`**
Adds a new key-value entry to the cache.

#### JSON Request Format:
```json
{
  "key": "your_key",
  "value": "your_value"
}
```

#### Sample Response:
```json
{
  "status": "OK",
  "key": "testKey",
  "value": "testValue"
}
```

#### Example using cURL:
```bash
curl -X POST 'http://127.0.0.1:7171/put' \
  -H 'Content-Type: application/json' \
  -d '{"key": "name", "value": "John"}'
```

---

### **GET `/get`**
Retrieves the value associated with a given key.

#### Query Parameter:
- `key`: The desired key to fetch.

#### Successful Response:
```json
{
  "value": "testValue"
}
```

#### If Key is Missing:
```json
{
  "status": "ERROR",
  "message": "Key not found."
}
```

#### cURL Example:
```bash
curl 'http://127.0.0.1:7171/get?key=name'
```

---

### **GET `/health`**
Returns the current status of the server.

#### Expected Output:
```json
{
  "status": "healthy"
}
```

#### Example cURL Command:
```bash
curl 'http://127.0.0.1:7171/health'
```

---

## Error Responses

- **404 Not Found**: Returned if the requested key does not exist in the cache.
- **400 Bad Request**: Returned if the key or value is too long (limit: 256 characters).