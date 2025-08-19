import json

class Settings:
    def __init__(self, path="config.json"):
        with open(path, "r") as f:
            self.config = json.load(f)

    def get(self, key: str, default=None):
        return self.config.get(key, default)

settings = Settings()