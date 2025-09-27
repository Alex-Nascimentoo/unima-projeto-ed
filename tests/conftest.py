import pytest

@pytest.fixture(autouse=True)
def setup_test():
    import random
    random.seed(42)