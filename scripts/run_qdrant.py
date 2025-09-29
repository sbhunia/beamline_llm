from qdrant_client import QdrantClient
from fastapi import FastAPI
import uvicorn

# Start Qdrant in-memory (can be persisted to disk later)
client = QdrantClient(":memory:")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Qdrant is running locally"}

# Optional: expose Qdrant-like API
# (for real-world usage, you'd mock endpoints or proxy here)

if __name__ == "__main__":
    print("Running Qdrant-compatible API server at http://localhost:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
