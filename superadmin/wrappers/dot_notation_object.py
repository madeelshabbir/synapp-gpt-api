class DotNotationObject:
    def __init__(self, data):
        self.data = data

    def __getattr__(self, name):
        if name in self.data:
            return self.data[name]
        raise AttributeError(f"'DotNotationObject' object has no attribute '{name}'")
