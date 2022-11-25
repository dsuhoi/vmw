import pytest
from app import create_app
from app.models import Articles


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


@pytest.mark.parametrize(
    "title, result", [("deriv", "$z(x, y), x y$"), ("diff", "$y'(y(x), x)$")]
)
def test_database(title, result):
    assert result in Articles.query.filter(Articles.title == title).all()[0].content
