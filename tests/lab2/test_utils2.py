import os
import tempfile
from unittest.mock import Mock

import pytest

from lab2.md5 import MD5
from lab2.utils2 import save_to_file, check_file_integrity, run_md5_tests


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


def test_save_to_file(temp_dir):
    """Test saving content to a file."""
    file_path = os.path.join(temp_dir, "test.txt")
    content = "Test content"

    save_to_file(file_path, content)

    # Verify file contents
    with open(file_path, 'r') as f:
        saved_content = f.read()

    assert saved_content == content


def test_check_file_integrity_valid(temp_dir):
    """Test file integrity checking with matching hashes."""
    # Create test file
    file_path = os.path.join(temp_dir, "test.txt")
    content = "Test content"
    save_to_file(file_path, content)

    # Calculate hash and save it
    md5 = MD5()
    hash_value = md5.hash_file(file_path)
    hash_file_path = os.path.join(temp_dir, "test.md5")
    save_to_file(hash_file_path, hash_value)

    # Check integrity
    assert check_file_integrity(file_path, hash_file_path) is True


def test_check_file_integrity_invalid(temp_dir):
    """Test file integrity checking with non-matching hashes."""
    # Create test file
    file_path = os.path.join(temp_dir, "test.txt")
    content = "Test content"
    save_to_file(file_path, content)

    # Save incorrect hash
    hash_file_path = os.path.join(temp_dir, "test.md5")
    save_to_file(hash_file_path, "incorrect_hash")

    # Check integrity
    assert check_file_integrity(file_path, hash_file_path) is False


def test_check_file_integrity_with_progress_callback(temp_dir):
    """Test file integrity checking with progress callback."""
    # Create test file
    file_path = os.path.join(temp_dir, "test.txt")
    content = "Test content"
    save_to_file(file_path, content)

    # Calculate and save hash
    md5 = MD5()
    hash_value = md5.hash_file(file_path)
    hash_file_path = os.path.join(temp_dir, "test.md5")
    save_to_file(hash_file_path, hash_value)

    # Create mock callback
    mock_callback = Mock()

    # Check integrity with callback
    result = check_file_integrity(file_path, hash_file_path, mock_callback)

    assert result is True
    assert mock_callback.call_count > 0  # Verify callback was called


def test_run_md5_tests():
    """Test the MD5 test runner function."""
    results = run_md5_tests()

    # Check that results contain all test cases
    assert "Input: ''" in results  # Empty string test
    assert "Input: 'abc'" in results  # Basic string test
    assert "Input: 'message digest'" in results  # With space
    assert "Correct: True" in results  # At least one correct result

    # Verify all test cases pass
    assert "Correct: False" not in results


def test_save_to_file_with_unicode(temp_dir):
    """Test saving content with unicode characters."""
    file_path = os.path.join(temp_dir, "unicode.txt")
    content = "Test content with unicode: 你好, 안녕하세요, Привет"

    save_to_file(file_path, content)

    with open(file_path, 'r', encoding='utf-8') as f:
        saved_content = f.read()

    assert saved_content == content


def test_check_file_integrity_case_insensitive(temp_dir):
    """Test that hash comparison is case-insensitive."""
    file_path = os.path.join(temp_dir, "test.txt")
    content = "Test content"
    save_to_file(file_path, content)

    # Calculate hash and save it in uppercase
    md5 = MD5()
    hash_value = md5.hash_file(file_path).upper()
    hash_file_path = os.path.join(temp_dir, "test.md5")
    save_to_file(hash_file_path, hash_value)

    # Should pass even though original hash might be in different case
    assert check_file_integrity(file_path, hash_file_path) is True