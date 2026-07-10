import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

CONFIG_FILE = "djinn.json"

DEFAULT_CONFIG = {
    "registry_url": "__bundled__",
    "style": "default",
    "tailwind": {
        "config": "tailwind.config.js",
        "css": "static/css/base.css",
        "cssVariables": True
    },
    "aliases": {
        "components": "templates/components",
        "utils": "theme/templatetags"
    },
    "registries": {}
}

class Config:
    def __init__(self, **kwargs):
        self.data = kwargs

    @property
    def registries(self) -> Dict[str, Any]:
        return self.data.get("registries", DEFAULT_CONFIG["registries"])

    @property
    def registry_url(self) -> str:
        return self.data.get("registry_url", DEFAULT_CONFIG["registry_url"])
    
    @registry_url.setter
    def registry_url(self, value):
        self.data["registry_url"] = value

    @property
    def tailwind(self) -> Dict[str, Any]:
        return self.data.get("tailwind", DEFAULT_CONFIG["tailwind"])

    @property
    def aliases(self) -> Dict[str, str]:
        return self.data.get("aliases", DEFAULT_CONFIG["aliases"])

    @property
    def style(self) -> str:
        return self.data.get("style", DEFAULT_CONFIG["style"])

    @classmethod
    def load(cls) -> Optional['Config']:
        if not os.path.exists(CONFIG_FILE):
            return None

        try:
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
                return cls(**data)
        except (json.JSONDecodeError, IOError):
            return None

    def save(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)

    @classmethod
    def init(cls) -> 'Config':
        config = cls(**DEFAULT_CONFIG.copy())
        config.save()
        return config

    def get_template_path(self) -> Path:
        return Path(self.aliases.get("components", DEFAULT_CONFIG["aliases"]["components"]))

    def get_python_path(self) -> Path:
        return Path(self.aliases.get("utils", DEFAULT_CONFIG["aliases"]["utils"]))
