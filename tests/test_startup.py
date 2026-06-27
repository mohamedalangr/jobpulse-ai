import pytest
from unittest.mock import patch
from src.services.startup import startup
from src.services.health import check_health, HealthStatus
from src.core.exceptions import DatabaseConnectionError

def test_health_check_database_mocked():
    """Verify health check returns healthy when DB connection succeeds."""
    with patch("src.services.health.check_connection") as mock_conn:
        mock_conn.return_value = True
        status = check_health()
        assert status.database is True
        assert status.configuration is True

def test_startup_success_mocked():
    """Verify startup completes without exception when all systems are healthy."""
    with patch("src.services.startup.check_health") as mock_health:
        mock_health.return_value = HealthStatus(
            database=True,
            configuration=True,
            logging=True,
            directories=True
        )
        result = startup()
        assert result.database_connected is True
        assert result.configuration_loaded is True

def test_startup_database_failure():
    """Verify startup raises DatabaseConnectionError when DB is unreachable."""
    with patch("src.services.startup.check_health") as mock_health:
        mock_health.return_value = HealthStatus(
            database=False,
            configuration=True,
            logging=True,
            directories=True
        )
        with pytest.raises(DatabaseConnectionError):
            startup()
