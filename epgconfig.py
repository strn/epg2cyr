# -*- coding: utf-8 -*-

import json, os, sys
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s - %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding='utf-8',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

class Config():
    
    def __init__(self, config_path='', program='program'):
        # Determine config file path
        if os.path.exists(config_path):
            with open(config_path) as fh:
                self.config = json.load(fh)
                logging.info(f"Configuration loaded from file '{config_path}' passed as parameter")
        else:
            # Config path does not exist, try loading from first program's argument
            self.config_path = os.path.join(os.getcwd(), f"{program}.json")
            if os.path.exists(self.config_path):
                with open(self.config_path) as fh:
                    self.config = json.load(fh)
                    logging.info(f"Configuration loaded from default configuration file '{self.config_path}'")
            else:
                logging.error(f"Neither default configuration file '{self.config_path}' exists nor it was provided via command line, aborting")
                exit(1)

    def getkey(self, key):
        return self.config[key]
    
    def get(self):
        return self.config

    def keys(self):
        return self.config.keys()
    
    def values(self):
        return self.config.values()

    def __repr__(self) -> str:
        return str(self.config)