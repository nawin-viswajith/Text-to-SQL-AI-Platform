from app.graph.nodes.execution import _classify_error


def test_classify_schema_mismatch() -> None:
    error = _classify_error("Unknown column 'foo' in 'field list'")
    assert error.category == "schema_mismatch"
    assert error.retryable is True


def test_classify_permission_error() -> None:
    error = _classify_error("Access denied for user 'readonly'")
    assert error.category == "permission"
    assert error.retryable is False


def test_classify_timeout_error() -> None:
    error = _classify_error("Query timeout while reading rows")
    assert error.category == "timeout"
    assert error.retryable is True

