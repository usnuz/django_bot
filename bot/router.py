import inspect

from .types import TelegramObject
from .states import StateManager


class Router:
    def __init__(self, bot):
        self.bot = bot
        self.handlers = {}
        self.error_handlers = {}
        self.state_handlers = {}

    def __call__(self, event_type, condition=None, state=None):
        def decorator(handler):
            if event_type == 'error':
                name = condition.__name__
                self.error_handlers[name] = (condition, handler)
                return handler
            elif state:
                if event_type not in self.handlers:
                    self.handlers[event_type] = []
                self.handlers[event_type].append({"condition": condition, "handler": handler, "state": state})
            else:
                if event_type not in self.handlers:
                    self.handlers[event_type] = []
                self.handlers[event_type].append({"condition": condition, "handler": handler})
                return handler
        return decorator

    def updater(self, update):
        event_type, data = self.detect_event_type(update)
        data = TelegramObject(data)
        if event_type in self.handlers:
            state = StateManager(event_type, data)
            for handlers in self.handlers[event_type]:
                if handlers.get("state"):
                    condition, handler, st = handlers.values()
                    if (condition is None or condition(data)) and st == state.current():
                        keys = inspect.signature(handler).parameters.keys()
                        if 'state' in keys:
                            handler(data, state)
                        else:
                            handler(data)
                        break
                else:
                    condition, handler = handlers.values()
                    if condition is None or condition(data):
                        keys = inspect.signature(handler).parameters.keys()
                        if 'state' in keys:
                            handler(data, state)
                        else:
                            handler(data)
                        break


    @staticmethod
    def detect_event_type(update):
        if "message" in update:
            return "message", update["message"]
        elif "callback_query" in update:
            return "callback_query", update["callback_query"]
        elif "inline_query" in update:
            return "inline_query", update["inline_query"]
        return None, None

