from unittest.mock import patch

import pytest

from lab1.lcg import LCG


@pytest.fixture
def mock_config():
    return {
        'a': 1664525,
        'c': 1013904223,
        'm': 2**32,
        'seed': 12345
    }

@pytest.fixture
def lcg_instance(mock_config):
    with patch('lab1.lcg.read_config') as mock_read:
        mock_read.return_value = (
            mock_config['a'],
            mock_config['c'],
            mock_config['m'],
            mock_config['seed']
        )
        return LCG()

def test_lcg_initialization(lcg_instance, mock_config):
    assert lcg_instance.a == mock_config['a']
    assert lcg_instance.c == mock_config['c']
    assert lcg_instance.m == mock_config['m']
    assert lcg_instance.seed == mock_config['seed']
    assert lcg_instance.current == mock_config['seed']

def test_lcg_next(lcg_instance, mock_config):
    expected = (mock_config['a'] * mock_config['seed'] + mock_config['c']) % mock_config['m']
    assert lcg_instance.next() == expected

def test_lcg_reset(lcg_instance, mock_config):
    lcg_instance.next()  # Change current value
    lcg_instance.reset()
    assert lcg_instance.current == mock_config['seed']

def test_generate_sequence(lcg_instance):
    sequence = lcg_instance.generate_sequence(5)
    assert len(sequence) == 5
    assert all(isinstance(x, int) for x in sequence)