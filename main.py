#!/usr/bin/env python
import os

from app import create_app

app = create_app(os.getenv("APP_SETTINGS") or "config.development_config")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
