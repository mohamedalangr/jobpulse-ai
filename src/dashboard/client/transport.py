import requests
import uuid
from urllib.parse import urljoin
from src.dashboard.config import settings
from src.dashboard.client.exceptions import ApiClientError
import streamlit as st

class Transport:
    def __init__(self):
        self.base_url = settings.api_url
        self.timeout = settings.request_timeout

    def _get_api_key(self) -> str:
        # Pull dynamically from session state if available
        if "api_key" in st.session_state and st.session_state.api_key:
            return st.session_state.api_key
        return settings.api_key

    def _build_headers(self) -> dict:
        request_id = str(uuid.uuid4())
        correlation_id = str(uuid.uuid4())
        return {
            "Content-Type": "application/json",
            "X-API-Key": self._get_api_key(),
            "X-Request-ID": request_id,
            "X-Correlation-ID": correlation_id
        }

    def _handle_response(self, response: requests.Response) -> dict:
        if 200 <= response.status_code < 300:
            return response.json()
            
        # Try to parse the standard JSON envelope
        try:
            error_payload = response.json()
            error_data = error_payload.get("error", {})
            message = error_data.get("message", f"Unknown API Error (Status {response.status_code})")
            details = error_data.get("details", {})
        except ValueError:
            message = f"HTTP {response.status_code} Error: {response.text}"
            details = {}

        raise ApiClientError(message=message, status_code=response.status_code, details=details)

    def get(self, endpoint: str, params: dict = None) -> dict:
        url = urljoin(f"{self.base_url}/", endpoint.lstrip("/"))
        try:
            response = requests.get(
                url, 
                headers=self._build_headers(), 
                params=params, 
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ApiClientError(message=f"Network Error: Unable to reach {self.base_url}", status_code=503)

    def post(self, endpoint: str, json_data: dict = None) -> dict:
        url = urljoin(f"{self.base_url}/", endpoint.lstrip("/"))
        try:
            response = requests.post(
                url, 
                headers=self._build_headers(), 
                json=json_data, 
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ApiClientError(message=f"Network Error: Unable to reach {self.base_url}", status_code=503)
