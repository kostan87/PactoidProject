def assert_dict_subset(actual: dict, expected: dict) -> None:
    for key, value in expected.items():
        assert key in actual, f"Missing key: {key!r}"
        assert actual[key] == value, (f"Key {key!r}: expected {value!r}, got {actual[key]!r}")