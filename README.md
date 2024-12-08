# LLM

[![PyPI](https://img.shields.io/pypi/v/llm.svg)](https://pypi.org/project/llm/)
[![Documentation](https://readthedocs.org/projects/llm/badge/?version=latest)](https://llm.datasette.io/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm?include_prereleases&label=changelog)](https://llm.datasette.io/en/stable/changelog.html)
[![Tests](https://github.com/simonw/llm/workflows/Test/badge.svg)](https://github.com/simonw/llm/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm/blob/main/LICENSE)
[![Discord](https://img.shields.io/discord/823971286308356157?label=discord)](https://datasette.io/discord-llm)

A CLI utility and Python library for interacting with Large Language Models, including OpenAI, PaLM and local models installed on your own machine.

Full documentation: **[llm.datasette.io](https://llm.datasette.io/)**

Background on this project:
- [llm, ttok and strip-tags—CLI tools for working with ChatGPT and other LLMs](https://simonwillison.net/2023/May/18/cli-tools-for-llms/)
- [The LLM CLI tool now supports self-hosted language models via plugins](https://simonwillison.net/2023/Jul/12/llm/)
- [Accessing Llama 2 from the command-line with the llm-replicate plugin](https://simonwillison.net/2023/Jul/18/accessing-llama-2/)

## Installation

Install this tool using `pip`:
```bash
pip install llm
```
Or using [Homebrew](https://brew.sh/):
```bash
brew install llm
```
[Detailed installation instructions](https://llm.datasette.io/en/stable/setup.html).

## Getting started

If you have an [OpenAI API key](https://platform.openai.com/account/api-keys) you can get started using the OpenAI models right away.

As an alternative to OpenAI, you can [install plugins](https://llm.datasette.io/en/stable/plugins/installing-plugins.html) to access models by other providers, including models that can be installed and run on your own device.

Save your OpenAI API key like this:

```bash
llm keys set openai
```
This will prompt you for your key like so:
```bash
llm keys set openai
```
```
Enter key: <paste here>
```
Now that you've saved a key you can run a prompt like this:
```bash
llm "Five cute names for a pet penguin"
```
```
1. Waddles
2. Pebbles
3. Bubbles
4. Flappy
5. Chilly
```
Read the [usage instructions](https://llm.datasette.io/en/stable/usage.html) for more.

## Using a system prompt

You can use the `-s/--system` option to set a system prompt, providing instructions for processing other input to the tool.

To describe how the code a file works, try this:

```bash
cat mycode.py | llm -s "Explain this code"
```

## Help

For help, run:

    llm --help

You can also use:

    python -m llm --help
