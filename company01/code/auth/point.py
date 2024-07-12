# Point of a finite group

class Point:
    def __init__(self, value):
        self._value = value
    def __repr__(self):
        return f"Point({self._value})"