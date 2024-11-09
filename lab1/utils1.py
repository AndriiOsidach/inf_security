import math
import random
from pathlib import Path

import numpy as np


def read_config():
    script_dir = Path(__file__).parent
    config_path = script_dir / 'config.txt'
    config = {}
    with open(config_path, "r") as f:
        for line in f:
            key, value = line.strip().split('=')
            config[key] = eval(value)
    return config['a'], config['c'], config['m'], config['seed']


def generate_system_sequence(n):
    return [random.randint(7**3 + 89, 2**20 - 1) for _ in range(n)]


def calculate_period(sequence):
    seen = set()
    for i, value in enumerate(sequence):
        if value in seen:
            return i
        seen.add(value)
    return len(sequence)


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def estimate_pi(sequence):
    if len(sequence) < 2:
        return "Not enough random numbers to estimate."

    count = 0
    total = 0
    for i in range(0, len(sequence) - 1, 2):
        x, y = sequence[i], sequence[i + 1]
        if gcd(x, y) == 1:
            count += 1
        total += 1
    probability = count / total
    if probability == 0:
        return np.inf
    return math.sqrt(6 / probability)
