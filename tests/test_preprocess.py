from src.preprocess import preprocess_text


def test_preprocess_normalizes_common_skill_aliases():
    text = "Python dev with ML, JS, and Postgres experience."

    processed = preprocess_text(text)

    assert "machine learn" in processed
    assert "javascript" in processed
    assert "postgresql" in processed
