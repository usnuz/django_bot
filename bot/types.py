from datetime import datetime, time, date
from collections.abc import Iterable

class TelegramObject:
    def __init__(self, data: dict):
        for key, value in data.items():
            if isinstance(value, dict):
                value = TelegramObject(value)
            elif isinstance(value, list):
                value = [TelegramObject(item) if isinstance(item, dict) else item for item in value]
            value = self.convert_special_types(value)
            setattr(self, key, value)

    @staticmethod
    def convert_special_types(value):
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                pass
            try:
                return time.fromisoformat(value)
            except ValueError:
                pass
            try:
                return date.fromisoformat(value)
            except ValueError:
                pass
        if isinstance(value, tuple):
            return tuple(value)
        if isinstance(value, set):
            return set(value)
        if isinstance(value, Iterable) and not isinstance(value, str):
            return list(value)
        return value