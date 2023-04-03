import pygame
import os
import json

class KeyConfig:
    def __init__(self, config_file="keyconfig.json"):
        self.config_file = config_file
        self.default_config = {
            "up": pygame.K_UP,
            "down": pygame.K_DOWN,
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "enter": pygame.K_RETURN,
            "space": pygame.K_SPACE
        }
        self.config = self.load_config()

    def load_config(self):
        if os.path.isfile(self.config_file):
            with open(self.config_file, "r") as f:
                config = json.load(f)
        else:
            config = self.default_config
            self.save_config(config)
        return config

    def save_config(self, config):
        with open(self.config_file, "w") as f:
            json.dump(config, f)

    def update_key(self, action, key_code):
        self.config[action] = key_code
        self.save_config(self.config)

    def get_key(self, action):
        return self.config.get(action, None)
