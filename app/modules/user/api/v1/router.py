#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter
from app.modules.user.api.v1 import login, register, user

v1 = APIRouter()

v1.include_router(login.router, prefix='', tags=['用户管理'])
v1.include_router(register.router, prefix='', tags=['用户管理'])
v1.include_router(user.router, prefix='', tags=['用户管理'])
