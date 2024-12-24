import pytest
import llm
from llm.plugins import pm


def pytest_configure(config):
    import sys

    sys._called_from_test = True


@pytest.fixture
def user_path(tmpdir):
    dir = tmpdir / "llm.datasette.io"
    dir.mkdir()
    return dir


@pytest.fixture
def templates_path(user_path):
    dir = user_path / "templates"
    dir.mkdir()
    return dir


@pytest.fixture(autouse=True)
def env_setup(monkeypatch, user_path):
    monkeypatch.setenv("LLM_USER_PATH", str(user_path))


class EmbedDemo(llm.EmbeddingModel):
    model_id = "embed-demo"

    def embed(self, text):
        words = text.split()[:16]
        embedding = [len(word) for word in words]
        # Pad with 0 up to 16 words
        embedding += [0] * (16 - len(embedding))
        return embedding


@pytest.fixture(autouse=True)
def register_embed_demo_model():
    class EmbedDemoPlugin:
        __name__ = "EmbedDemoPlugin"

        @llm.hookimpl
        def register_embedding_models(self, register):
            register(EmbedDemo())

    pm.register(EmbedDemoPlugin(), name="undo-embed-demo-plugin")
    try:
        yield
    finally:
        pm.unregister(name="undo-embed-demo-plugin")


@pytest.fixture
def mocked_openai(requests_mock):
    return requests_mock.post(
        "https://api.openai.com/v1/chat/completions",
        json={
            "model": "gpt-3.5-turbo",
            "usage": {},
            "choices": [{"message": {"content": "Bob, Alice, Eve"}}],
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def mocked_localai(requests_mock):
    return requests_mock.post(
        "http://localai.localhost/chat/completions",
        json={
            "model": "orca",
            "usage": {},
            "choices": [{"message": {"content": "Bob, Alice, Eve"}}],
        },
        headers={"Content-Type": "application/json"},
    )
