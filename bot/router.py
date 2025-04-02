from .types import TelegramObject


class Router:
    def __init__(self, bot):
        self.bot = bot
        self.handlers = {}
        self.error_handlers = {}

    def __call__(self, event_type, filter1=None):
        def decorator(handler):
            if event_type == 'error':
                name = filter1.__name__
                self.error_handlers[name] = (filter1, handler)
                return handler
            else:
                if event_type not in self.handlers:
                    self.handlers[event_type] = []
                self.handlers[event_type].append((filter1, handler))
                return handler
        return decorator

    def updater(self, update):
        event_type, data = self.detect_event_type(update)
        data = TelegramObject(data)
        if event_type in self.handlers:
            for filter1, handler in self.handlers[event_type]:
                if filter1(data):
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

