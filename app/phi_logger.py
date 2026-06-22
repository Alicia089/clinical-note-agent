import json
import logging
from datetime import datetime, timezone


class PHISafeLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(message)s"))
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def _emit(self, level: str, event: str, **kwargs) -> None:
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": level,
            "event": event,
            **kwargs,
        }
        getattr(self.logger, level.lower())(json.dumps(record))

    def info(self, event: str, **kwargs) -> None:
        self._emit("INFO", event, **kwargs)

    def error(self, event: str, **kwargs) -> None:
        self._emit("ERROR", event, **kwargs)
