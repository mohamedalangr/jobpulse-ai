from pytest_archon import archrule

def test_domain_is_isolated():
    """Domain layer must not depend on any outer layers."""
    (
        archrule("Domain Layer Isolation")
        .match("src.domain.*")
        .should_not_import("src.application.*")
        .should_not_import("src.api.*")
        .should_not_import("src.dashboard.*")
        .should_not_import("sqlalchemy.*")
        .check("src")
    )

def test_application_layer_dependencies():
    """Application layer depends on domain, but not API or Dashboard."""
    (
        archrule("Application Layer Dependencies")
        .match("src.application.*")
        .should_not_import("src.api.*")
        .should_not_import("src.dashboard.*")
        .check("src")
    )

def test_dashboard_is_isolated():
    """Dashboard must be a pure HTTP client and not import backend logic."""
    (
        archrule("Dashboard Independence")
        .match("src.dashboard.*")
        .should_not_import("src.domain.*")
        .should_not_import("src.application.*")
        .should_not_import("src.api.*")
        .should_not_import("src.database.*")
        .should_not_import("sqlalchemy.*")
        .check("src")
    )
