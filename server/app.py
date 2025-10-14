#!/usr/bin/python3


"""app main entry point"""
from fastapi import FastAPI
from server.routes import router as api_router

import os
from server import crud


app = FastAPI()
app.include_router(api_router)


@app.on_event("startup")
def ensure_admin_user():
    """If there are no accounts and ADMIN_USER/ADMIN_PASS are set, create an admin.

    This is a convenience for first-run local development only. For production,
    set up users via migrations or a secure admin flow and ensure secrets are
    provided via a secrets manager.
    """
    try:
        items = crud.list_accounts(limit=1)
    except Exception:
        items = []
    if not items:
        admin_user = os.environ.get("ADMIN_USER")
        admin_pass = os.environ.get("ADMIN_PASS")
        admin_email = os.environ.get("ADMIN_EMAIL")
        if admin_user and admin_pass:
            try:
                crud.create_account(username=admin_user, password=admin_pass,
                                    email=admin_email, role="admin")
                print("Created initial admin user from ADMIN_USER/ADMIN_PASS")
            except Exception as e:
                print("Failed to create admin user:", e)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)