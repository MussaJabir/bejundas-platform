import pytest

from apps.core.models import SiteSettings


@pytest.mark.django_db
class TestSiteSettings:
    def test_get_creates_singleton(self):
        obj = SiteSettings.get()
        assert obj is not None
        assert obj.company_name == "Bejundas Group of Companies"

    def test_get_returns_same_instance(self):
        obj1 = SiteSettings.get()
        obj2 = SiteSettings.get()
        assert str(obj1.pk) == str(obj2.pk)

    def test_str(self):
        obj = SiteSettings.get()
        assert str(obj) == obj.company_name
