from fastapi import FastAPI
import os
import uvicorn

app = FastAPI()

# Get configuration from environment variables
APP_VERSION = os.getenv('APP_VERSION', 'unknown')
PORT = int(os.getenv('PORT', '8080'))

@app.get("/")
def read_root():
    return {
        "message": "Hello World",
        "version": APP_VERSION
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=False)
