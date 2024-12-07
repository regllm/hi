(python-api)=
# Python API

LLM provides a Python API for executing prompts, in addition to the command-line interface.

Understanding this API is also important for writing {ref}`plugins`.

## Basic prompt execution

To run a prompt against the `gpt-3.5-turbo` model, run this:

```python
import llm

model = llm.get_model("gpt-3.5-turbo")
model.key = 'YOUR_API_KEY_HERE'
response = model.prompt("Five surprising names for a pet pelican")
print(response.text())
```
The `llm.get_model()` function accepts model names or aliases - so `chatgpt` would work here too.

Run this command to see a list of available models and their aliases:

```bash
llm models list
```
If you have set a `OPENAI_API_KEY` environment variable you can omit the `model.key = ` line.

### System prompts

For models that accept a system prompt, pass it as `system="..."`:

```python
response = model.prompt(
    "Five surprising names for a pet pelican",
    system="Answer like GlaDOS"
)
```

### Models from plugins

Any models you have installed as plugins will also be available through this mechanism, for example to use Google's PaLM 2 model with [llm-palm](https://github.com/simonw/llm-palm)

```bash
pip install llm-palm
```
```python
import llm

model = llm.get_model("palm")
model.key = 'YOUR_API_KEY_HERE'
response = model.prompt("Five surprising names for a pet pelican")
print(response.text())
```
You can omit the `model.key = ` line for models that do not use an API key

## Streaming responses

For models that support it you can stream responses as they are generated, like this:

```python
response = model.prompt("Five diabolical names for a pet goat")
for chunk in response:
    print(chunk, end="")
```
The `response.text()` method described earlier does this for you - it runs through the iterator and gathers the results into a string.

If a response has been evaluated, `response.text()` will continue to return the same string.

## Conversations

LLM supports *conversations*, where you ask follow-up questions of a model as part of an ongoing conversation.

To start a new conversation, use the `model.conversation()` method:

```python
model = llm.get_model("gpt-3.5-turbo")
model.key = 'YOUR_API_KEY_HERE'
conversation = model.conversation()
```
You can then use the `conversation.prompt()` method to execute prompts against this conversation:

```python
response = conversation.prompt("Five fun facts about pelicans")
print(response.text())
```
This works exactly the same as the `model.prompt()` method, except that the conversation will be maintained across multiple prompts. So if you run this next:
```python
response2 = conversation.prompt("Now do skunks")
print(response2.text())
```
You will get back five fun facts about skunks.

Access `conversation.responses` for a list of all of the responses that have so far been returned during the conversation.
