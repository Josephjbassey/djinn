import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

CONFIG_FILE = "djinn.config.json"

DEFAULT_CONFIG = {
    "registry_url": "__bundled__",
    "output": {
        "templates": "templates/components",
        "python": "templatetags"
    }
}

class Config:
    def __init__(self, registry_url: str, output: Dict[str, str]):
        self.registry_url = registry_url
        self.output = output

    @classmethod
    def load(cls) -> Optional['Config']:
        if not os.path.exists(CONFIG_FILE):
            return None

        try:
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
                return cls(
                    registry_url=data.get("registry_url", DEFAULT_CONFIG["registry_url"]),
                    output=data.get("output", DEFAULT_CONFIG["output"])
                )
        except (json.JSONDecodeError, IOError):
            return None

    def save(self):
        data = {
            "registry_url": self.registry_url,
            "output": self.output
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=2)

    @classmethod
    def init(cls) -> 'Config':
        config = cls(
            registry_url=DEFAULT_CONFIG["registry_url"],
            output=DEFAULT_CONFIG["output"]
        )
        config.save()
        return config

    def get_template_path(self) -> Path:
        return Path(self.output.get("templates", DEFAULT_CONFIG["output"]["templates"]))

    def get_python_path(self) -> Path:
        return Path(self.output.get("python", DEFAULT_CONFIG["output"]["python"]))
