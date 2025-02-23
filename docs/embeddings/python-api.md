(embeddings-python-api)=
# Using embeddings from Python

You can load an embedding model using its model ID or alias like this:
```python
import llm

embedding_model = llm.get_embedding_model("3-small")
```
To embed a string, returning a Python list of floating point numbers, use the `.embed()` method:
```python
vector = embedding_model.embed("my happy hound")
```
If the embedding model can handle binary input, you can call `.embed()` with a byte string instead. You can check the `supports_binary` property to see if this is supported:
```python
if embedding_model.supports_binary:
    vector = embedding_model.embed(open("my-image.jpg", "rb").read())
```
The `embedding_model.supports_text` property indicates if the model supports text input.

Many embeddings models are more efficient when you embed multiple strings or binary strings at once. To embed multiple strings at once, use the `.embed_multi()` method:
```python
vectors = list(embedding_model.embed_multi(["my happy hound", "my dissatisfied cat"]))
```
This returns a generator that yields one embedding vector per string.

Embeddings are calculated in batches. By default all items will be processed in a single batch, unless the underlying embedding model has defined its own preferred batch size. You can pass a custom batch size using `batch_size=N`, for example:

```python
vectors = list(embedding_model.embed_multi(lines_from_file, batch_size=20))
```

(embeddings-python-collections)=
## Working with collections

The `llm.Collection` class can be used to work with **collections** of embeddings from Python code.

A collection is a named group of embedding vectors, each stored along with their IDs in a SQLite database table.

To work with embeddings in this way you will need an instance of a [sqlite-utils Database](https://sqlite-utils.datasette.io/en/stable/python-api.html#connecting-to-or-creating-a-database) object. You can then pass that to the `llm.Collection` constructor along with the unique string name of the collection and the ID of the embedding model you will be using with that collection:

```python
import sqlite_utils
import llm

# This collection will use an in-memory database that will be
# discarded when the Python process exits
collection = llm.Collection("entries", model_id="3-small")

# Or you can persist the database to disk like this:
db = sqlite_utils.Database("my-embeddings.db")
collection = llm.Collection("entries", db, model_id="3-small")

# You can pass a model directly using model= instead of model_id=
embedding_model = llm.get_embedding_model("3-small")
collection = llm.Collection("entries", db, model=embedding_model)
```
If the collection already exists in the database you can omit the `model` or `model_id` argument - the model ID will be read from the `collections` table.

To embed a single string and store it in the collection, use the `embed()` method:

```python
collection.embed("hound", "my happy hound")
```
This stores the embedding for the string "my happy hound" in the `entries` collection under the key `hound`.

Add `store=True` to store the text content itself in the database table along with the embedding vector.

To attach additional metadata to an item, pass a JSON-compatible dictionary as the `metadata=` argument:

```python
collection.embed("hound", "my happy hound", metadata={"name": "Hound"}, store=True)
```
This additional metadata will be stored as JSON in the `metadata` column of the embeddings database table.

(embeddings-python-bulk)=
### Storing embeddings in bulk

The `collection.embed_multi()` method can be used to store embeddings for multiple items at once. This can be more efficient for some embedding models.

```python
collection.embed_multi(
    [
        ("hound", "my happy hound"),
        ("cat", "my dissatisfied cat"),
    ],
    # Add this to store the strings in the content column:
    store=True,
)
```
To include metadata to be stored with each item, call `embed_multi_with_metadata()`:

```python
collection.embed_multi_with_metadata(
    [
        ("hound", "my happy hound", {"name": "Hound"}),
        ("cat", "my dissatisfied cat", {"name": "Cat"}),
    ],
    # This can also take the store=True argument:
    store=True,
)
```
The `batch_size=` argument defaults to 100, and will be used unless the embedding model itself defines a lower batch size. You can adjust this if you are having trouble with memory while embedding large collections:

```python
collection.embed_multi(
    (
        (i, line)
        for i, line in enumerate(lines_in_file)
    ),
    batch_size=10
)
```

(embeddings-python-collection-class)=
### Collection class reference

A collection instance has the following properties and methods:

- `id` - the integer ID of the collection in the database
- `name` - the string name of the collection (unique in the database)
- `model_id` - the string ID of the embedding model used for this collection
- `model()` - returns the `EmbeddingModel` instance, based on that `model_id`
- `count()` - returns the integer number of items in the collection
- `embed(id: str, text: str, metadata: dict=None, store: bool=False)` - embeds the given string and stores it in the collection under the given ID. Can optionally include metadata (stored as JSON) and store the text content itself in the database table.
- `embed_multi(entries: Iterable, store: bool=False, batch_size: int=100)` - see above
- `embed_multi_with_metadata(entries: Iterable, store: bool=False, batch_size: int=100)` - see above
- `similar(query: str, number: int=10)` - returns a list of entries that are most similar to the embedding of the given query string
- `similar_by_id(id: str, number: int=10)` - returns a list of entries that are most similar to the embedding of the item with the given ID
- `similar_by_vector(vector: List[float], number: int=10, skip_id: str=None)` - returns a list of entries that are most similar to the given embedding vector, optionally skipping the entry with the given ID
- `delete()` - deletes the collection and its embeddings from the database

There is also a `Collection.exists(db, name)` class method which returns a boolean value and can be used to determine if a collection exists or not in a database:

```python
if Collection.exists(db, "entries"):
    print("The entries collection exists")
```

(embeddings-python-similar)=
## Retrieving similar items

Once you have populated a collection of embeddings you can retrieve the entries that are most similar to a given string using the `similar()` method.

This method uses a brute force approach, calculating distance scores against every document. This is fine for small collections, but will not scale to large collections. See [issue 216](https://github.com/simonw/llm/issues/216) for plans to add a more scalable approach via vector indexes provided by plugins.

```python
for entry in collection.similar("hound"):
    print(entry.id, entry.score)
```
The string will first by embedded using the model for the collection.

The `entry` object returned is an object with the following properties:

- `id` - the string ID of the item
- `score` - the floating point similarity score between the item and the query string
- `content` - the string text content of the item, if it was stored - or `None`
- `metadata` - the dictionary (from JSON) metadata for the item, if it was stored - or `None`

This defaults to returning the 10 most similar items. You can change this by passing a different `number=` argument:
```python
for entry in collection.similar("hound", number=5):
    print(entry.id, entry.score)
```
The `similar_by_id()` method takes the ID of another item in the collection and returns the most similar items to that one, based on the embedding that has already been stored for it:

```python
for entry in collection.similar_by_id("cat"):
    print(entry.id, entry.score)
```
The item itself is excluded from the results.

(embeddings-sql-schema)=
## SQL schema

Here's the SQL schema used by the embeddings database:

<!-- [[[cog
import cog
from llm.embeddings_migrations import embeddings_migrations
import sqlite_utils
import re
db = sqlite_utils.Database(memory=True)
embeddings_migrations.apply(db)

cog.out("```sql\n")
for table in ("collections", "embeddings"):
    schema = db[table].schema
    cog.out(format(schema))
    cog.out("\n")
cog.out("```\n")
]]] -->
```sql
CREATE TABLE [collections] (
   [id] INTEGER PRIMARY KEY,
   [name] TEXT,
   [model] TEXT
)
CREATE TABLE "embeddings" (
   [collection_id] INTEGER REFERENCES [collections]([id]),
   [id] TEXT,
   [embedding] BLOB,
   [content] TEXT,
   [content_blob] BLOB,
   [content_hash] BLOB,
   [metadata] TEXT,
   [updated] INTEGER,
   PRIMARY KEY ([collection_id], [id])
)
```
<!-- [[[end]]] -->
