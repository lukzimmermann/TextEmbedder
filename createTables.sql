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
	last_modified_date TIMESTAMP
);

CREATE TABLE tag (
	doc_id INTEGER NOT NULL,
	tag TEXT NOT NULL
);

ALTER TABLE tag
ADD CONSTRAINT pk_tag PRIMARY KEY (doc_id,tag);
