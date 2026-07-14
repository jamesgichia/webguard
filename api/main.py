"""
FastAPI application entrypoint.
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import auth, dashboard, health, keys, reports, scans

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="WebGuard API",
    description="Passive OWASP Top 10 Web Vulnerability Scanner API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1/health", tags=["Health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(keys.router, prefix="/api/v1/keys", tags=["API Keys"])
app.include_router(scans.router, prefix="/api/v1/scans", tags=["Scans"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])
