from __future__ import annotations

from app.db.introspection import MySQLIntrospector
from app.db.mysql_client import MySQLClient
from app.rag.chroma_client import ChromaSchemaStore


class SchemaIndexer:
    def __init__(self, mysql_client: MySQLClient, chroma_store: ChromaSchemaStore) -> None:
        self.introspector = MySQLIntrospector(mysql_client=mysql_client)
        self.chroma_store = chroma_store

    def refresh(self, table_names: list[str] | None = None) -> int:
        docs = self.introspector.snapshot_tables(table_names=table_names)
        return self.chroma_store.upsert(docs)

