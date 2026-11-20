from pathlib import Path
import json
import yaml
from pyflow.utils import logger

class ConfigManager:
    def __init__(self,config_path:str="config/pipeline.yaml"):
        self.config_path =Path(config_path)
        self.data = self._load_config()
    def _load_config(self)->dict:
        if not self.config_path.exists():
            msg=f"Config file not found :{self.config_path}"
            logger.error(msg)
            raise FileNotFoundError(msg)

        ext=self.config_path.suffix.lower().strip()
        logger.info(f"Loading configuration from {self.config_path}")

        try:
            with open(self.config_path,"r",encoding="utf-8")as f:
                if ext in (".yaml",".yml"):
                    parsed = yaml.safe_load(f) or {}
                elif ext ==".json":
                    parsed = json.load(f) or {}
                else:
                    msg =f"Unsupported config format:{ext} (use .yaml, yml,or .json)"
                    logger.error(msg)
                    raise ValueError(msg)


            if not isinstance(parsed,dict):
                msg="Config root must be a mapping /dictionary"
                logger.error(msg)
                raise ValueError(msg)
            logger.info("Configuration loaded successfully")
            return parsed

        except Exception as e:
            logger.error(f"failed to load config {self.config_path}:{e}")
            raise

    def get(self, section: str, key: str = None, default=None):  # Section ya nested key safely nikalne ke liye
        section_data = self.data.get(section)  # 'data' dictionary se section nikala
        if section_data is None:  # Agar YAML mein section khali/None hai toh 'None' ke bajaye {} ya default lenge
            return {} if key is None else default  # Key nahi maangi toh {}, maangi hai toh default return kiya

        if key is None:  # Agar poora section dict chahiye
            return section_data if isinstance(section_data, dict) else (default if default is not None else {})  # Section dict return kiya

        if not isinstance(section_data, dict):  # Agar section dict nahi hai toh safe fallback
            return default  # Default value return ki

        return section_data.get(key, default)  # Key ki value ya default return kiya