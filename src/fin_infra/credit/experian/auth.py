"""OAuth 2.0 token management for Experian API.

Handles:
- Token acquisition via client credentials flow
- Token caching (in-memory, 1 hour TTL)
- Automatic token refresh before expiry
- Thread-safe token access

Example:
    >>> auth = ExperianAuthManager(
    ...     client_id="your_client_id",
    ...     client_secret="your_client_secret",
    ...     base_url="https://sandbox.experian.com"
    ... )
    >>> token = await auth.get_token()
    >>> # Use token in API calls
"""

import asyncio
import base64
from datetime import datetime, timedelta
from typing import Literal

import httpx


class ExperianAuthManager:
    """Manages OAuth 2.0 tokens for Experian API.
    
    Uses client credentials flow to obtain access tokens. Tokens are cached
    in memory and automatically refreshed before expiry.
    
    Args:
        client_id: Experian API client ID
        client_secret: Experian API client secret
        base_url: Experian API base URL (sandbox or production)
        token_ttl: Token validity in seconds (default: 3600)
        
    Attributes:
        _token: Current access token (None if not acquired)
        _token_expiry: Token expiry timestamp
        _lock: asyncio.Lock for thread-safe token refresh
    """

    def __init__(
        self,
        *,
        client_id: str,
        client_secret: str,
        base_url: str,
        token_ttl: int = 3600,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url.rstrip("/")
        self.token_ttl = token_ttl

        # Token state
        self._token: str | None = None
        self._token_expiry: datetime | None = None
        self._lock = asyncio.Lock()

    async def get_token(self) -> str:
        """Get valid access token, refreshing if needed.
        
        Thread-safe. If token is expired or about to expire (within 5 minutes),
        automatically refreshes before returning.
        
        Returns:
            Valid OAuth 2.0 access token
            
        Raises:
            httpx.HTTPStatusError: If token acquisition fails
            
        Example:
            >>> token = await auth.get_token()
            >>> headers = {"Authorization": f"Bearer {token}"}
        """
        async with self._lock:
            # Check if token is valid and not expiring soon
            if self._token and self._is_valid():
                return self._token

            # Refresh token
            await self._refresh_token()
            return self._token  # type: ignore

    def _is_valid(self) -> bool:
        """Check if current token is valid and not expiring soon.
        
        Returns:
            True if token exists and expires in more than 5 minutes
        """
        if not self._token or not self._token_expiry:
            return False

        # Refresh if expiring within 5 minutes
        buffer = timedelta(minutes=5)
        return datetime.utcnow() + buffer < self._token_expiry

    async def _refresh_token(self) -> None:
        """Acquire new access token from Experian OAuth endpoint.
        
        Uses client credentials flow:
        1. Encode client_id:client_secret as base64
        2. POST to /oauth2/v1/token with grant_type=client_credentials
        3. Extract access_token and expires_in from response
        4. Cache token with expiry timestamp
        
        Raises:
            httpx.HTTPStatusError: If token request fails (401, 500, etc.)
        """
        # Encode credentials as base64
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()

        # Request token
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/oauth2/v1/token",
                headers={
                    "Authorization": f"Basic {encoded}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data={
                    "grant_type": "client_credentials",
                    "scope": "read:credit write:credit",
                },
                timeout=10.0,
            )
            response.raise_for_status()

        # Parse response
        data = response.json()
        self._token = data["access_token"]
        expires_in = data.get("expires_in", self.token_ttl)
        self._token_expiry = datetime.utcnow() + timedelta(seconds=expires_in)

    async def invalidate(self) -> None:
        """Invalidate current token (force refresh on next get_token call).
        
        Useful when token is rejected by API (e.g., revoked, invalid).
        
        Example:
            >>> try:
            ...     await client.get("/endpoint")
            ... except httpx.HTTPStatusError as e:
            ...     if e.response.status_code == 401:
            ...         await auth.invalidate()
            ...         # Retry with new token
        """
        async with self._lock:
            self._token = None
            self._token_expiry = None
