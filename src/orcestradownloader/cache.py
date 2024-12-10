from pathlib import Path
from datetime import datetime
import json
from typing import Optional, List

from orcestradownloader.logging_config import logger as log

class Cache:
    def __init__(self, cache_dir: Path, cache_file: str, cache_days_to_keep: int = 7):
        self.cache_dir = cache_dir
        self.cache_file = cache_dir / cache_file
        self.cache_days_to_keep = cache_days_to_keep

    def get_cached_response(self) -> Optional[List[dict]]:
        """Retrieve cached response if it exists and is up-to-date."""
        log.debug("Checking for cached response...")
        if not self.cache_file.exists():
            log.info("Cache file not found.")
            return None
        try:
            with self.cache_file.open("r") as f:
                cached_data = json.load(f)
            cache_date = datetime.fromisoformat(cached_data["date"])
            if (datetime.now() - cache_date).days <= self.cache_days_to_keep:
                diff = datetime.now() - cache_date
                if diff.days > 0:
                    daysago = f"{diff.days} days ago"
                else:
                    minutes = diff.seconds // 60
                    hours = minutes // 60
                    if hours > 0:
                        daysago = f"{hours} hours ago"
                    else:
                        daysago = f"{minutes} minutes ago"
                log.info("Using cached response from %s", daysago)
                return cached_data["data"]
            else:
                log.info("Cache is outdated.")
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            log.warning("Failed to load cache: %s", e)
        return None

    def cache_response(self, data: List[dict]):
        """Save the response to the cache."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        with self.cache_file.open("w") as f:
            json.dump({"date": datetime.now().isoformat(), "data": data}, f)
        log.info("Response cached successfully.")