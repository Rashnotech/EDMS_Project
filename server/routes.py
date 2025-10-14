#!/usr/bin/python3
"""FastAPI routes for EDMS server"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import List
from server import crud
from server import schemas
from server.auth import create_access_token, verify_password, SECRET_KEY, ALGORITHM
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

router = APIRouter()


def get_current_user_from_token(token: str = Depends(oauth2_scheme)):
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		username: str = payload.get("sub")
		if username is None:
			raise HTTPException(status_code=401, detail="Invalid auth token")
	except JWTError:
		raise HTTPException(status_code=401, detail="Invalid auth token")

	user = crud.get_account_by_username(username)
	if not user:
		raise HTTPException(status_code=401, detail="User not found")
	return user


@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
	user = crud.get_account_by_username(form_data.username)
	if not user or not verify_password(form_data.password, user.password_hash):
		raise HTTPException(status_code=400, detail="Incorrect username or password")

	access_token = create_access_token({"sub": user.username})
	return {"access_token": access_token, "token_type": "bearer"}


@router.post("/accounts", response_model=schemas.AccountRead)
def create_account(account: schemas.AccountCreate, current_user=Depends(get_current_user_from_token)):
	# only admin can create new accounts
	if current_user.role != "admin":
		raise HTTPException(status_code=403, detail="Insufficient permissions")

	try:
		a = crud.create_account(
			username=account.username,
			password=account.password,
			email=account.email,
			role=account.role or "staff",
		)
	except ValueError as e:
		if str(e) == "username_exists":
			raise HTTPException(status_code=400, detail="Username already exists")
		raise HTTPException(status_code=500, detail=str(e))
	return a.to_dict()


@router.get("/accounts", response_model=List[schemas.AccountRead])
def list_accounts(current_user=Depends(get_current_user_from_token)):
	# only admin can list all accounts
	if current_user.role != "admin":
		raise HTTPException(status_code=403, detail="Insufficient permissions")
	items = crud.list_accounts()
	return [i.to_dict() for i in items]


@router.get("/accounts/{account_id}", response_model=schemas.AccountRead)
def get_account(account_id: int, current_user=Depends(get_current_user_from_token)):
	acct = crud.get_account_by_id(account_id)
	if not acct:
		raise HTTPException(status_code=404, detail="Account not found")
	# allow admins or the user themselves
	if current_user.role != "admin" and current_user.id != acct.id:
		raise HTTPException(status_code=403, detail="Insufficient permissions")
	return acct.to_dict()


@router.put("/accounts/{account_id}", response_model=schemas.AccountRead)
def update_account(account_id: int, updates: schemas.AccountUpdate, current_user=Depends(get_current_user_from_token)):
	acct = crud.get_account_by_id(account_id)
	if not acct:
		raise HTTPException(status_code=404, detail="Account not found")
	if current_user.role != "admin" and current_user.id != acct.id:
		raise HTTPException(status_code=403, detail="Insufficient permissions")

	data = {k: v for k, v in updates.dict().items() if v is not None}
	acct = crud.update_account(account_id, data)
	if not acct:
		raise HTTPException(status_code=404, detail="Account not found")
	return acct.to_dict()


@router.delete("/accounts/{account_id}")
def delete_account(account_id: int, current_user=Depends(get_current_user_from_token)):
	# only admin can delete accounts
	if current_user.role != "admin":
		raise HTTPException(status_code=403, detail="Insufficient permissions")
	ok = crud.delete_account(account_id)
	if not ok:
		raise HTTPException(status_code=404, detail="Account not found")
	return {"deleted": True}

