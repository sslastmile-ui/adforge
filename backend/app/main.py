import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from .database import create_tables
from .routes import briefs, generate, khadakx_webhook

# Create database tables
create_tables()

app = FastAPI(title="AdForge AI API", version="1.0.0")

# CORS - Allow all origins for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(briefs.router, prefix="/api/briefs", tags=["briefs"])
app.include_router(generate.router, prefix="/api/generate", tags=["generate"])
app.include_router(khadakx_webhook.router, prefix="/api/webhooks/khadakx", tags=["khadakx"])


@app.get("/")
def root():
    return {"message": "AdForge AI API is running!"}


@app.get("/api/health")
def health():
    return {"status": "healthy", "service": "AdForge API"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
