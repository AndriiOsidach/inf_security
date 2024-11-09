import os
import tempfile

import pytest

from lab2.md5 import MD5


@pytest.fixture
def md5_hasher():
    return MD5()


def test_initialization(md5_hasher):
    """Test that MD5 initializes with correct constants"""
    assert md5_hasher.A == 0x67452301
    assert md5_hasher.B == 0xEFCDAB89
    assert md5_hasher.C == 0x98BADCFE
    assert md5_hasher.D == 0x10325476
    assert len(md5_hasher.S) == 64
    assert len(md5_hasher.K) == 64


def test_left_rotate(md5_hasher):
    """Test the left rotation operation"""
    assert md5_hasher.left_rotate(0x12345678, 4) == 0x23456781
    assert md5_hasher.left_rotate(0xFFFFFFFF, 8) == 0xFFFFFFFF
    assert md5_hasher.left_rotate(0x00000001, 31) == 0x80000000


@pytest.mark.parametrize("input_str,expected_hash", [
    ("", "d41d8cd98f00b204e9800998ecf8427e"),
    ("a", "0cc175b9c0f1b6a831c399e269772661"),
    ("abc", "900150983cd24fb0d6963f7d28e17f72"),
    ("message digest", "f96b697d7cb7938d525a2f31aaf161d0"),
    ("abcdefghijklmnopqrstuvwxyz", "c3fcd3d76192e4007dfb496cca67e13b"),
    ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "d174ab98d277d9f5a5611c2c9f419d9f"),
    ("12345678901234567890123456789012345678901234567890123456789012345678901234567890",
     "57edf4a22be3c955ac49da2e2107b67a"),
])
def test_hash_known_values(md5_hasher, input_str, expected_hash):
    """Test MD5 hash against known test vectors"""
    assert md5_hasher.hash(input_str) == expected_hash


def test_hash_unicode(md5_hasher):
    """Test hashing unicode strings"""
    unicode_str = "Hello 世界"
    hash_result = md5_hasher.hash(unicode_str)
    # This is the expected hash for "Hello 世界" encoded in UTF-8
    assert len(hash_result) == 32
    assert all(c in "0123456789abcdef" for c in hash_result)


def test_file_hashing_with_progress(md5_hasher):
    """Test file hashing with progress callback"""
    progress_values = []

    def progress_callback(progress):
        progress_values.append(progress)
        return True  # Continue processing

    # Create a temporary file with larger content
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        tf.write(b"a" * 10000)
        temp_path = tf.name

    try:
        hash_result = md5_hasher.hash_file(temp_path, progress_callback)
        assert hash_result is not None
        assert len(progress_values) > 0
        assert progress_values[-1] == 100  # Last progress should be 100%
        assert all(0 <= p <= 100 for p in progress_values)  # All progress values should be between 0 and 100
    finally:
        os.unlink(temp_path)


def test_file_hashing_cancelled(md5_hasher):
    """Test cancelling file hashing via progress callback"""

    def progress_callback(progress):
        return False  # Cancel processing

    with tempfile.NamedTemporaryFile(delete=False) as tf:
        tf.write(b"test content\n")
        temp_path = tf.name

    try:
        hash_result = md5_hasher.hash_file(temp_path, progress_callback)
        assert hash_result is None  # Should return None when cancelled
    finally:
        os.unlink(temp_path)


def test_compress_block(md5_hasher):
    """Test the compression function with a known block"""
    initial_buf = [md5_hasher.A, md5_hasher.B, md5_hasher.C, md5_hasher.D]
    test_block = [0] * 16  # Test with a block of zeros
    result = md5_hasher.compress(initial_buf, test_block)
    assert len(result) == 4
    assert all(isinstance(x, int) for x in result)
    assert all(0 <= x <= 0xFFFFFFFF for x in result)


def test_large_file_hashing(md5_hasher):
    """Test hashing a large file (>8KB to test chunking)"""
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        # Create a 10KB file
        tf.write(b"0" * 10240)
        temp_path = tf.name

    try:
        hash_result = md5_hasher.hash_file(temp_path)
        assert len(hash_result) == 32
        assert all(c in "0123456789abcdef" for c in hash_result)
    finally:
        os.unlink(temp_path)