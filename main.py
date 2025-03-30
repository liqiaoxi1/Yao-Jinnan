from fastapi import FastAPI, status, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from fastapi.staticfiles import StaticFiles
from app.router import route
import uvicorn
from database.database import init_db  # 导入 init_db 函数
import asyncio
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

description_text = """
FastAPI 项目模板
"""
app = FastAPI(
    title="FastAPI 项目模板",
    openapi_url="/openapi.json",
    description=description_text,
    version=settings.API_VERSION,   
    contact=settings.CONTACT,
    terms_of_service="https://www.ktechhub.com/terms/",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境替换为settings.ALLOWED_HOSTS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
        初始化数据库表，在应用启动时执行
    """
    await init_db()


@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url="/docs")
@app.get("/ready", status_code=status.HTTP_200_OK, include_in_schema=True)
async def ready() -> str:
    """Check if API it's ready"""
    return "ready"


# 将版本管理路由器包括到FastAPI主应用中
app.include_router(route)

# 静态文件存放在项目的 "static" 目录下
app.mount("/i", StaticFiles(directory="static"), name="internal-static")


if __name__ == "__main__":
    asyncio.run(init_db())
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.RELOAD)  # TODO 根据环境设置reload参数


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"验证错误详情: {exc.errors()}")  # 打印详细错误信息
    return JSONResponse(
        status_code=422,
        content={
            "detail": [
                {
                    "loc": err["loc"],
                    "msg": err["msg"],
                    "type": err["type"]
                }
                for err in exc.errors()
            ]
        }
    )