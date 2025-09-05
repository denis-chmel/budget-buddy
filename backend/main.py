import os
import subprocess
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.api.auth import router as auth_router
from backend.api.health import router as health_router
from backend.api.transactions import router as transactions_router
from backend.core.settings import settings

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    database_url = settings.database_url

    if database_url:
        try:
            result = subprocess.run([
                'yoyo', 'apply', '--batch',
                '--database', database_url,
                'backend/db/migrations'
            ], capture_output=True, text=True, check=True, timeout=60)
            logger.info("Migrations applied successfully")
            if result.stdout:
                logger.info(f"Migration output: {result.stdout}")

        except subprocess.TimeoutExpired:
            logger.error("Migration timed out after 60 seconds")
        except subprocess.CalledProcessError as e:
            logger.error(f"Migration failed: {e}")
            logger.error(f"stdout: {e.stdout}")
            logger.error(f"stderr: {e.stderr}")
        except Exception as e:
            logger.error(f"Unexpected migration error: {e}")
    else:
        logger.warning("No DATABASE_URL found, skipping migrations")

    yield

    logger.info("App is shutting down...")

app = FastAPI(lifespan=lifespan, debug=settings.debug_mode)
app.include_router(health_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(transactions_router, prefix="/api")

app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")
