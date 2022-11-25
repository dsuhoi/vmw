import pytest
from app import create_app


@pytest.fixture(scope="module")
def client():
    app = create_app("config.development_config")
    with app.test_client() as _client:
        yield _client


@pytest.mark.parametrize(
    "url, result",
    [
        ("/", "ВИРТУАЛЬНЫЙ МАТЕМАТИЧЕСКИЙ ПРАКТИКУМ"),
        ("/post", "<p><h2>Статьи</h2></p>"),
        ("/programs", ""),
    ],
)
def test_check_page(client, url, result):
    resp = client.get(url, follow_redirects=True)
    assert resp.status_code == 200
    assert result in resp.data.decode("utf-8")
