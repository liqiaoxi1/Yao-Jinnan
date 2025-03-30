# conftest.py 配置文件

import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        yield client

@pytest.fixture
def mock_auth_header():
    # 模拟认证头
    return {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsImlzX3JlZnJlc2giOmZhbHNlLCJwYXNzd29yZCI6IiQyYiQxMiRHL1RCYWUvbExyMFJkY0VUWnBFMC5lM0NzMm1iZ3RGVm5RL1JQRW1OOWhKV2k2L3BWU2t1ZSIsImV4cCI6MTczMTIzMDU5OX0.ouNA3k74qgBHkkAT_cyFs1lIhOQdzpAGO-w4h1C4G9M"
    }

@pytest.fixture
def test_client():
    return TestClient(app)
