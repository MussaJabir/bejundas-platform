"""Tests for the app_theme context processor — verifies per-vertical
theming and legal_name resolution."""

import pytest
from django.test import RequestFactory

from apps.core.context_processors import app_theme


class _FakeMatch:
    def __init__(self, app_name="", kwargs=None):
        self.app_name = app_name
        self.kwargs = kwargs or {}


def _request_with_match(app_name="", kwargs=None):
    req = RequestFactory().get("/")
    req.resolver_match = _FakeMatch(app_name=app_name, kwargs=kwargs)
    return req


class TestAppThemeLegalName:
    def test_construction_returns_bejus_legal_entity(self):
        theme = app_theme(_request_with_match(app_name="construction"))["app_theme"]
        assert theme["legal_name"] == "BEJUS SERVICES ENGINEERING & CONSTRUCTION (T) LTD"
        assert theme["primary"] == "#2c2c2c"
        assert theme["accent"] == "#f47920"

    def test_financial_returns_bfs_legal_entity(self):
        theme = app_theme(_request_with_match(app_name="financial"))["app_theme"]
        assert theme["legal_name"] == "BEJUNDAS FINANCIAL SERVICES LTD"
        assert theme["primary"] == "#0a2342"
        assert theme["accent"] == "#c9a84c"

    def test_hub_default_has_empty_legal_name(self):
        theme = app_theme(_request_with_match(app_name="hub"))["app_theme"]
        assert theme["legal_name"] == ""
        assert theme["label"] == "Bejundas Group"

    def test_vertical_kwarg_takes_precedence_over_app_name(self):
        theme = app_theme(
            _request_with_match(app_name="leads", kwargs={"vertical": "construction"})
        )["app_theme"]
        assert theme["legal_name"] == "BEJUS SERVICES ENGINEERING & CONSTRUCTION (T) LTD"

    def test_unknown_app_falls_back_to_group_default(self):
        theme = app_theme(_request_with_match(app_name="totally-unknown"))["app_theme"]
        assert theme["label"] == "Bejundas Group"
        assert theme["legal_name"] == ""

    def test_no_resolver_match_falls_back(self):
        req = RequestFactory().get("/")
        # No resolver_match attached at all
        theme = app_theme(req)["app_theme"]
        assert theme["label"] == "Bejundas Group"

    @pytest.mark.parametrize(
        "vertical",
        ["energies", "farming", "investments"],
    )
    def test_other_verticals_have_legal_name_slot_for_later(self, vertical):
        """Slot exists but is empty until those verticals ship."""
        theme = app_theme(_request_with_match(app_name=vertical))["app_theme"]
        assert "legal_name" in theme
        assert theme["legal_name"] == ""
