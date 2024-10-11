from click.testing import CliRunner
from llm.cli import cli
import json
import pytest
import sqlite_utils


def test_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert result.output.startswith("cli, version ")


@pytest.fixture
def log_path(tmp_path):
    path = str(tmp_path / "log.db")
    db = sqlite_utils.Database(path)
    db["log"].insert_all(
        {
            "command": "chatgpt",
            "system": "system",
            "prompt": "prompt",
            "response": "response",
            "model": "davinci",
        }
        for i in range(100)
    )
    return path


@pytest.mark.parametrize("n", (None, 0, 2))
def test_logs(n, log_path):
    runner = CliRunner()
    args = ["logs", "-p", log_path]
    if n is not None:
        args.extend(["-n", str(n)])
    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    logs = json.loads(result.output)
    expected_length = 3
    if n is not None:
        if n == 0:
            expected_length = 100
        else:
            expected_length = n
    assert len(logs) == expected_length
