from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import create_tables
from .routes import briefs, generate
import uvicorn

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

@app.get("/")
def root():
    return {"message": "AdForge AI API is running!"}

@app.get("/api/health")
def health():
    return {"status": "healthy", "service": "AdForge API"}

if __name__ == "__main__":
    uvicorn.run(app, host="10.10.11.73", port=8000)