from sqlalchemy import Table, Column, Integer, String, ForeignKey, TIMESTAMP, Boolean, MetaData

metadata = MetaData()

file = Table(
    "file",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("path", String, unique=True),
    Column("author", String),
    Column("public", Boolean),
    Column("created_at", TIMESTAMP(True)),
    Column("likes", Integer)
)

favourites = Table(
    "favourites",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("id_file", ForeignKey(file.c.id)),
    Column("user_id", Integer)
)