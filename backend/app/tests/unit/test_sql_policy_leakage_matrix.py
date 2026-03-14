import pytest

from app.core.security import SQLPolicy, SQLPolicyError


UNSAFE_QUERIES = [
    "UPDATE users SET active = 1",
    "DELETE FROM users WHERE id = 1",
    "DROP TABLE users",
    "ALTER TABLE users ADD COLUMN x INT",
    "INSERT INTO users(id) VALUES (1)",
    "TRUNCATE TABLE users",
    "CREATE TABLE x(id INT)",
    "GRANT SELECT ON db.* TO user",
]


@pytest.mark.parametrize("query", UNSAFE_QUERIES)
def test_unsafe_queries_are_blocked(query: str) -> None:
    policy = SQLPolicy(default_limit=100, max_limit=1000)
    with pytest.raises(SQLPolicyError):
        policy.validate_and_harden(query)

