import json
import os


class Config:
    chance = {}

    def __init__(self, config_path):
        self.config_path = config_path
        self.load_config()

    def load_config(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf8') as config_file:
                    self.chance = json.load(config_file)
            else:
                self.chance = {}
        except:
            self.chance = {}

    def save_config(self):
        with open(self.config_path, 'w', encoding='utf8') as config_file:
            json.dump(self.chance, config_file, ensure_ascii=False, indent=4)

    def set_chance(self, gid, chance):
        self.chance[gid] = chance
        self.save_config()

    def delete_chance(self, gid):
        if gid in self.chance:
            del self.chance[gid]
            self.save_config()

