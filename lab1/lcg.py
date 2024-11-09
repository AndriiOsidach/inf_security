from lab1.utils1 import (read_config)


class LCG:
    def __init__(self):
        self.a, self.c, self.m, self.seed = read_config()
        self.current = self.seed

    def next(self):
        self.current = (self.a * self.current + self.c) % self.m
        return self.current

    def reset(self):
        self.current = self.seed

    def generate_sequence(self, n):
        return [self.next() for _ in range(n)]
