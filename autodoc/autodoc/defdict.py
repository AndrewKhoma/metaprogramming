class Defdict(dict):
    def __missing__(self, key):
        return None
