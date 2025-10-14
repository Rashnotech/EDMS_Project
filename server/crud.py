#!/usr/bin/python3
"""CRUD helpers for server models (Account)."""
from typing import Optional, Dict, Any, List
from server import storage
from server.account import Account
from server.auth import hash_password, verify_password as _verify_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against the stored hash."""
    return _verify_password(plain_password, hashed_password)


def create_account(username: str, password: str, email: Optional[str] = None,
                   role: str = "staff", status: str = "active") -> Account:
    """Create and persist a new Account.

    Raises ValueError if username already exists.
    """
    existing = get_account_by_username(username)
    if existing:
        raise ValueError("username_exists")

    account = Account()
    account.username = username
    account.email = email
    account.password_hash = hash_password(password)
    account.role = role
    account.status = status

    # persist via storage
    storage.new(account)
    storage.save()
    return account


def get_account_by_id(account_id: int) -> Optional[Account]:
    """Retrieve an Account by its id."""
    try:
        return storage.get(Account, account_id)
    except Exception:
        # storage.get may raise if misconfigured; return None in that case
        return None


def get_account_by_username(username: str) -> Optional[Account]:
    """Retrieve an Account by username."""
    sess = getattr(storage, "_DBStorage__session", None)
    if sess is None:
        return None
    try:
        return sess.query(Account).filter_by(username=username).first()
    except Exception:
        return None


def update_account(account_id: int, updates: Dict[str, Any]) -> Optional[Account]:
    """Update fields on an account. Returns updated account or None.

    Supported update keys: username, email, password, role, status
    """
    acct = get_account_by_id(account_id)
    if not acct:
        return None

    if "username" in updates:
        acct.username = updates["username"]
    if "email" in updates:
        acct.email = updates["email"]
    if "password" in updates:
        acct.password_hash = hash_password(updates["password"])
    if "role" in updates:
        acct.role = updates["role"]
    if "status" in updates:
        acct.status = updates["status"]

    # commit
    storage.save()
    return acct


def delete_account(account_id: int) -> bool:
    """Delete an account by id. Returns True if deleted."""
    acct = get_account_by_id(account_id)
    if not acct:
        return False
    storage.delete(acct)
    storage.save()
    return True


def list_accounts(limit: Optional[int] = None, offset: int = 0) -> List[Account]:
    """Return a list of accounts. Uses underlying session for querying."""
    sess = getattr(storage, "_DBStorage__session", None)
    if sess is None:
        return []
    q = sess.query(Account).order_by(Account.id)
    if offset:
        q = q.offset(offset)
    if limit:
        q = q.limit(limit)
    return q.all()
