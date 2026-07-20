from fastapi import FastAPI

app = FastAPI(
    title="Tattva AI",
    description="Evidence-Driven Incident Intelligence",
    version="1.0.0",
)

@app.get("/")
def root():
    return {
        "message": "Tattva AI Backend Running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }