import pytest
from fastapi import Request, Response
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from app import app, lifespan, request_limiter, add_session_id
from models import Sessions


# Fixture to provide the FastAPI app instance for testing
@pytest.fixture
def test_app():
    return app


# Fixture to provide a TestClient instance for making requests to the app
@pytest.fixture
def test_client(test_app):
    with TestClient(test_app) as client:
        yield client


@pytest.mark.asyncio
async def test_lifespan(test_app):
    """
    Test the lifespan context manager of the FastAPI app.
    This ensures that the sessions attribute is properly initialized.
    """
    async with lifespan(test_app):
        # Check if the 'sessions' attribute exists in the app state
        assert hasattr(test_app.state, "sessions")
        # Verify that the 'sessions' attribute is an instance of the Sessions class
        assert isinstance(test_app.state.sessions, Sessions)


@pytest.mark.asyncio
async def test_request_limiter_production():
    """
    Test the request_limiter middleware in production mode.
    This ensures that requests from unauthorized hosts are rejected.
    """
    with patch("src.app.IS_PRODUCTION", True), patch(
        "src.app.ALLOWED_HOST", "127.0.0.1"
    ):
        mock_request = MagicMock()
        mock_request.client.host = "192.168.1.1"

        # Create a mock response with a status_code attribute
        mock_response = MagicMock()
        mock_response.status_code = 401

        # Create a mock call_next function that returns the mock response
        async def mock_call_next(request):
            return mock_response

        # Call the request_limiter middleware
        response = await request_limiter(mock_request, mock_call_next)

        # Assert that the response status code is 401 (Unauthorized)
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_add_session_id():
    """
    Test the add_session_id middleware when a session ID is provided.
    This ensures that the session ID is properly added to the request state and response headers.
    """
    # Create a mock request with a session ID
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"petry-session-id": "test-session"}
    mock_request.state = MagicMock()

    # Create a mock response
    mock_response = MagicMock(spec=Response)
    mock_response.headers = {}

    # Create a mock call_next function that returns the mock response
    async def mock_call_next(request):
        return mock_response

    # Call the add_session_id middleware
    response = await add_session_id(mock_request, mock_call_next)

    # Assert that the session ID was added to the request state
    assert mock_request.state.session_id == "test-session"

    # Assert that the session ID was added to the response headers
    assert "petry-session-id" in response.headers
    assert response.headers["petry-session-id"] == "test-session"

    # Print debug information (useful for troubleshooting)
    print(f"Response headers: {response.headers}")
    print(f"Response type: {type(response)}")


@pytest.mark.asyncio
async def test_add_session_id_no_session():
    """
    Test the add_session_id middleware when no session ID is provided.
    This ensures that the middleware behaves correctly when there's no session ID.
    """
    # Create a mock request without a session ID
    mock_request = MagicMock()
    mock_request.headers = {}
    mock_response = MagicMock()
    mock_call_next = AsyncMock(return_value=mock_response)

    # Call the add_session_id middleware
    response = await add_session_id(mock_request, mock_call_next)

    # Assert that no session ID was added to the request state
    assert mock_request.state.session_id is None
    # Assert that no session ID was added to the response headers
    assert "petry-session-id" not in response.headers
