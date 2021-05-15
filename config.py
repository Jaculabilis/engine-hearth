'''
Filesystem-based config interface. This is not good design but it's very easy to use.
'''
import json
import os


class Config:
    def __init__(self, path):
        self.path = path

    def __getitem__(self, key):
        with open(self.path) as f:
            cfg = json.load(f)
            return cfg[key]

    def __setitem__(self, key, value):
        with open(self.path, 'w') as f:
            cfg = json.load(f)
            cfg[key] = value
            json.dump(cfg, f, indent=2)


EnvConfig = Config(os.environ.get('EH_CONFIG'))
