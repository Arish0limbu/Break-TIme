"""
Example test file for project validation.
"""

def test_example():
    """Example test case"""
    assert True

def test_configuration():
    """Test that configuration is accessible"""
    import config
    assert hasattr(config, 'MIN_COMMITS')
    assert hasattr(config, 'MAX_COMMITS')
    assert config.MIN_COMMITS >= 1
    assert config.MAX_COMMITS >= config.MIN_COMMITS

if __name__ == "__main__":
    test_example()
    test_configuration()
    print("All tests passed!")