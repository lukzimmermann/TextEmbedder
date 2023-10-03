# TextEmbedder

Creates embeddings using [text-embedding-ada-002](https://openai.com/blog/new-and-improved-embedding-model) from all PDF's that are in the folders and subfolders listed in a text file. These embeddings are then stored in a Postgres database with the [pgvector](https://github.com/pgvector/pgvector) extension.

This allows to find the relevant pages of all scanned PDF's via a prompt.

## How to use

Below is a brief explanation of how the project can be used.

### Install Python dependencies

Install all dependencies needed for this project:

```bash
pip install -r requirements.txt
```

### Filelist File

Add one or more lines containing a path. The file must be in the root directory of the project. Below is an example:

`filelist.txt`

```
/Users/Peter/Documents/School
/Users/Peter/Documents/Work
```

### .env

A token for the OpenAI Api is required. Furthermore, the credentials for the database are stored also here.

`.env`

```
OPENAI_ORGANISATION_ID = "OrganisationId"
OPENAI_API_KEY = "ApiToken"

DB_NAME = "postgres"
DB_USER = "user"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = 5432
```

### createTables.sql

This query creates all necessary tables in the database.

```sql
CREATE EXTENSION vector;

CREATE TABLE embedding (
	doc_id INTEGER,
	doc_segment INTEGER,
	doc_text TEXT,
	tokens INTEGER,
	embedding_ada002 vector(1536)
);

ALTER TABLE embedding
ADD CONSTRAINT pk_embedding PRIMARY KEY (doc_id,doc_segment, doc_text);

CREATE TABLE document (
	id SERIAL PRIMARY KEY,
	filename TEXT,
	path TEXT,
	last_modified_date INTEGER
);

CREATE TABLE tag (
	doc_id INTEGER NOT NULL,
	tag TEXT NOT NULL
);

ALTER TABLE tag
ADD CONSTRAINT pk_tag PRIMARY KEY (doc_id,tag);
```
