#!/usr/bin/python3
"""Pydantic schemas for server API"""
from pydantic import BaseModel, EmailStr
from typing import Optional


class AccountCreate(BaseModel):
	username: str
	password: str
	email: Optional[EmailStr] = None
	role: Optional[str] = "staff"


class AccountUpdate(BaseModel):
	username: Optional[str] = None
	password: Optional[str] = None
	email: Optional[EmailStr] = None
	role: Optional[str] = None
	status: Optional[str] = None


class AccountRead(BaseModel):
	id: int
	username: str
	email: Optional[EmailStr] = None
	role: str
	status: str
	created_at: Optional[str] = None
	updated_at: Optional[str] = None

	class Config:
		orm_mode = True
