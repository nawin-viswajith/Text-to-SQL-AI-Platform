from app.core.security import SQLPolicy, SQLPolicyError


def test_sql_policy_blocks_update() -> None:
    policy = SQLPolicy(default_limit=100, max_limit=1000)
    try:
        policy.validate_and_harden("UPDATE users SET active = 1")
    except SQLPolicyError as exc:
        assert "Unsafe SQL operation" in str(exc)
    else:
        raise AssertionError("Expected SQLPolicyError for UPDATE query.")


def test_sql_policy_adds_default_limit() -> None:
    policy = SQLPolicy(default_limit=100, max_limit=1000)
    sql = policy.validate_and_harden("SELECT * FROM users")
    assert sql.endswith("LIMIT 100")


def test_sql_policy_caps_limit() -> None:
    policy = SQLPolicy(default_limit=100, max_limit=1000)
    sql = policy.validate_and_harden("SELECT * FROM users LIMIT 9999")
    assert sql.lower().endswith("limit 1000")

