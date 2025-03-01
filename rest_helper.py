"""Helper functions for making REST API calls."""

import requests
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def make_rest_call(
    base_url: str,
    method: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
) -> str:
    """
    Make a REST API call and return the response as a string.

    Args:
        base_url: The base URL for the API call
        method: HTTP method (GET, POST, PUT, DELETE, PATCH)
        headers: Optional headers for the request
        params: Optional parameters (query params for GET, body for POST/PUT)
        timeout: Request timeout in seconds

    Returns:
        String representation of the response (success or error)
    """
    try:
        response = requests.request(
            method=method,
            url=base_url,
            headers=headers or {},
            params=params if method == "GET" else None,
            json=params if method != "GET" and params else None,
            timeout=timeout,
        )

        # Try to get JSON response first, fall back to text
        try:
            result = response.json()
            return f"Status: {response.status_code}\nResponse: {result}"
        except ValueError:
            return f"Status: {response.status_code}\nResponse: {response.text}"

    except requests.RequestException as e:
        logger.error(f"REST call error: {str(e)}")
        return f"Error making REST call: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error in REST call: {str(e)}")
        return f"Unexpected error: {str(e)}"
