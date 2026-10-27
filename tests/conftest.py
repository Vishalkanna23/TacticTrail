
import json

import pytest
from fastapi.testclient import TestClient

from app import technique_search
from app.config import Settings, get_settings
from app.main import app


@pytest.fixture
def client():
    app.dependency_overrides[get_settings] = lambda: Settings(
        app_name="tactictrail",
        environment="test",
    )

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def technique_data(tmp_path, monkeypatch):
    data = [
        {
            "technique_id": "T1566.001",
            "name": "Spearphishing Attachment",
            "tactics": ["Initial Access"],
            "description": "Phishing using a malicious attachment",
            "url": "https://attack.mitre.org/techniques/T1566/001",
        }
    ]

    file_path = tmp_path / "techniques.json"
    file_path.write_text(
        json.dumps(data),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        technique_search,
        "DATA_FILE",
        file_path,
    )
