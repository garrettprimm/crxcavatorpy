import pytest
import requests
from crxcavator import api

extension_id = "lkhghipfmlbmmcamcamkhpjjggnlpani"
extension_version = "10.1.2"


class MockResponse:
    @staticmethod
    def json():
        return {"mock_key": "mock_response"}


@pytest.fixture
def mock_get_report(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_get_all_reports(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)


def test_get_report(mock_get_report):
    result = api.get_report(extension_id, extension_version)
    assert type(result) is dict


def test_get_all_reports(mock_get_report):
    result = api.get_report(extension_id, extension_version)
    assert type(result) is list
