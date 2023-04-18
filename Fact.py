import time

class Fact:
    def __init__(self, key, value, timestamp=None):
        self.key = key
        self.value = value
        self.timestamp = timestamp if timestamp else time.time()

    def __str__(self):
        return f"{self.key}: {self.value} @ {self.timestamp}"
