# Share of the secret value

class Share():
    def __init__(self, value):
        self._value = value
    def __repr__(self):
        return f"Share({self._value})"