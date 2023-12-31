import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from your_module_path.managerServices import router
from dbase import DB
import modules.model as _model


# Replace 'your_module_path' with the actual path where your managerServices.py module is located

@pytest.fixture
def app():
    # If you are using FastAPI's TestClient, you may set up your app here.
    # Example: from your_module_path.main import app
    # return app
    pass


@pytest.fixture
def client(app):
    # If you are using FastAPI's TestClient, you may set up your TestClient here.
    # Example: return TestClient(app)
    pass


@pytest.mark.asyncio
async def test_get_all_requests():
    # Assuming your DB module provides a fetch_all method
    with patch.object(DB, 'fetch_all', return_value=[{"id": 1, "name": "Request 1"}, {"id": 2, "name": "Request 2"}]):
        response = await client.get("/requests")
        assert response.status_code == 200
        assert response.json() == [{"id": 1, "name": "Request 1"}, {"id": 2, "name": "Request 2"}]


@pytest.mark.asyncio
async def test_get_request():
    # Assuming your DB module provides a fetch_one method
    with patch.object(DB, 'fetch_one', return_value={"id": 1, "name": "Request 1"}):
        response = await client.get("/requests/1")
        assert response.status_code == 200
        assert response.json() == {"id": 1, "name": "Request 1"}


@pytest.mark.asyncio
async def test_get_request_not_found():
    # Assuming your DB module provides a fetch_one method that returns None for non-existent requests
    with patch.object(DB, 'fetch_one', return_value=None):
        response = await client.get("/requests/999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Request not found"}


@pytest.mark.asyncio
async def test_confirm_status():
    # Assuming you have appropriate data and mock for the update method
    mock_execute = Mock()
    with patch.object(DB, 'execute', mock_execute):
        response = await client.put("/confirm", json={"user_id": 1, "datas_from_users": {"firstname": "John", "lastname": "Doe", "age": 25}})
        assert response.status_code == 200
        assert response.json() == {"message": "Status confirmed and user_info updated"}

        # Verify that the update method was called with the correct parameters
        mock_execute.assert_called_once_with(
            update(_model.requests).where(_model.requests.c.user_id == 1).values(is_done=True, confirmed=True)
        )


@pytest.mark.asyncio
async def test_reject_status():
    # Assuming you have appropriate data and mock for the update method
    mock_execute = Mock()
    with patch.object(DB, 'execute', mock_execute):
        response = await client.put("/reject", json={"user_id": 1})
        assert response.status_code == 200
        assert response.json() == {"message": "Request rejected"}

        # Verify that the update method was called with the correct parameters
        mock_execute.assert_called_once_with(
            update(_model.requests).where(_model.requests.c.user_id == 1).values(confirmed=False, is_done=True)
        )
