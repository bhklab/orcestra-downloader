import pytest
from pathlib import Path
import json
from datetime import datetime, timedelta
from orcestradownloader.cache import Cache

@pytest.fixture
def cache_dir(tmp_path):
    """Fixture to create a temporary directory for testing."""
    return tmp_path / "cache"

@pytest.fixture
def cache_file(cache_dir):
    """Fixture to return the cache file path."""
    return cache_dir / "test_cache.json"

@pytest.fixture
def sample_data():
    """Fixture to return sample data."""
    return [{"name": "Test", "value": 42}]

@pytest.fixture
def cache_instance(cache_dir, cache_file):
    """Fixture to return a Cache instance."""
    return Cache(cache_dir, cache_file.name, cache_days_to_keep=7)

def test_cache_file_creation(cache_instance, cache_dir, sample_data):
    """Test that the cache file is created and contains valid data."""
    cache_instance.cache_response(sample_data)
    assert cache_instance.cache_file.exists(), "Cache file was not created."

    with cache_instance.cache_file.open("r") as f:
        cached_data = json.load(f)
    
    assert "date" in cached_data, "Cache file is missing the 'date' field."
    assert "data" in cached_data, "Cache file is missing the 'data' field."
    assert cached_data["data"] == sample_data, "Cached data does not match the input data."

def test_get_cached_response_valid(cache_instance, sample_data):
    """Test that a valid cache is returned."""
    cache_instance.cache_response(sample_data)
    response = cache_instance.get_cached_response(name="Test")
    assert response == sample_data, "Cached response does not match the expected data."

def test_get_cached_response_outdated(cache_instance, cache_file, sample_data):
    """Test that an outdated cache returns None."""
    outdated_date = (datetime.now() - timedelta(days=8)).isoformat()
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    with cache_file.open("w") as f:
        json.dump({"date": outdated_date, "data": sample_data}, f)

    response = cache_instance.get_cached_response(name="Test")
    assert response is None, "Outdated cache should return None."

def test_get_cached_response_missing_file(cache_instance):
    """Test that a missing cache file returns None."""
    response = cache_instance.get_cached_response(name="Test")
    assert response is None, "Missing cache file should return None."

def test_get_cached_response_invalid_json(cache_instance, cache_file):
    """Test that an invalid JSON in the cache file is handled gracefully."""
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    with cache_file.open("w") as f:
        f.write("{invalid_json}")

    response = cache_instance.get_cached_response(name="Test")
    assert response is None, "Invalid JSON in the cache should return None."

def test_cache_file_outdated_handling(cache_instance, cache_file, sample_data, caplog):
    """Test the logging output when the cache is outdated."""
    caplog.set_level("INFO")
    outdated_date = (datetime.now() - timedelta(days=8)).isoformat()
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    with cache_file.open("w") as f:
        json.dump({"date": outdated_date, "data": sample_data}, f)

    response = cache_instance.get_cached_response(name="Test")
    assert response is None, "Outdated cache should return None."
    
    assert any("Cache is outdated" in record.message for record in caplog.records), \
        "Log message for outdated cache not found."

def test_cache_file_logging(cache_instance, sample_data, caplog):
    """Test that logging occurs when using a valid cache."""
    caplog.set_level("INFO")
    cache_instance.cache_response(sample_data)
    response = cache_instance.get_cached_response(name="Test")
    assert response == sample_data, "Cached response does not match the expected data."

    assert any("Using cached response" in record.message for record in caplog.records), \
        "Log message for valid cache not found."