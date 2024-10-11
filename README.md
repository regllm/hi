# llm

[![PyPI](https://img.shields.io/pypi/v/llm.svg)](https://pypi.org/project/llm/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm?include_prereleases&label=changelog)](https://github.com/simonw/llm/releases)
[![Tests](https://github.com/simonw/llm/workflows/Test/badge.svg)](https://github.com/simonw/llm/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm/blob/master/LICENSE)

Access large language models from the command-line

## Installation

Install this tool using `pip`:

    pip install llm

You need an OpenAI API key, which should either be set in the `OPENAI_API_KEY` environment variable, or saved in a plain text file called `~/.openai-api-key.txt` in your home directory.

## Usage

The default command for this is `llm chatgpt` - you can use `llm` instead if you prefer.

To run a prompt:

    llm 'Ten names for cheesecakes'

To stream the results a token at a time:

    llm 'Ten names for cheesecakes' -s

To switch from ChatGPT 3.5 (the default) to GPT-4 if you have access:

    llm 'Ten names for cheesecakes' -4

Pass `--model <model name>` to use a different model.

## Logging to SQLite

If a SQLite database file exists in `~/.llm/log.db` then the tool will log all prompts and responses to it.

You can create that file by running the `init-db` command:

    llm init-db

Now any prompts you run will be logged to that database.

To avoid logging a prompt, pass `--no-log` or `-n` to the command:

    llm 'Ten names for cheesecakes' -n

## Help

For help, run:

    llm --help

You can also use:

    python -m llm --help

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd llm
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
