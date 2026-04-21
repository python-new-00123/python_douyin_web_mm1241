from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys
import os
import aiomysql
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from crawlers.douyin.web.web_crawler import db_manager

router = APIRouter()


class CookieUpdateRequest(BaseModel):
    service: str
    cookie: str


class CookieResponse(BaseModel):
    success: bool
    message: str
    service: str = None
    cookie: str = None


@router.get("/{service}", response_model=CookieResponse)
async def get_cookie(service: str):
    try:
        cookie = db_manager.get_cookie(service)
        if cookie:
            return CookieResponse(
                success=True,
                message="Cookie retrieved successfully",
                service=service,
                cookie=cookie
            )
        else:
            return CookieResponse(
                success=False,
                message=f"No active cookie found for service: {service}",
                service=service
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=CookieResponse)
async def update_cookie(request: CookieUpdateRequest):
    try:
        db_manager.save_cookie(request.service, request.cookie)
        return CookieResponse(
            success=True,
            message=f"Cookie updated successfully for service: {request.service}",
            service=request.service
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{service}", response_model=CookieResponse)
async def delete_cookie(service: str):
    try:
        await db_manager.init_pool()
        async with db_manager.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    'UPDATE cookies SET is_active = 0 WHERE service = %s',
                    (service,)
                )
        
        return CookieResponse(
            success=True,
            message=f"Cookie deactivated successfully for service: {service}",
            service=service
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list/all", response_model=list)
async def list_all_cookies():
    try:
        await db_manager.init_pool()
        async with db_manager.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    'SELECT service, cookie, updated_at, is_active FROM cookies WHERE is_active = 1 ORDER BY updated_at DESC'
                )
                results = []
                for row in await cursor.fetchall():
                    results.append({
                        "service": row["service"],
                        "cookie": row["cookie"],
                        "updated_at": str(row["updated_at"]),
                        "is_active": bool(row["is_active"])
                    })
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
