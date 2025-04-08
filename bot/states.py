from typing import Optional


class StateManager:

    STATES = {}

    def __init__(self, event_type, data):
        if event_type == 'message':
            self.chat_id = data.chat.id,
            self.user_id = data.from_user.id,
        elif event_type == 'callback_query':
            self.chat_id = data.message.chat.id,
            self.user_id = data.message.from_user.id,
        if f'ID{self.chat_id}' not in self.STATES:
            self.STATES[f'ID{self.chat_id}'] = {}

    def set(self, name):
        self.STATES[f'ID{self.chat_id}'].update({'state': name})

    def update(self, data: dict) -> None:
        self.STATES[f'ID{self.chat_id}'].update({'data': data})

    def get(self):
        return self.STATES.get(f'ID{self.chat_id}').get('data', {})

    def clear(self):
        del self.STATES[f'ID{self.chat_id}']

    def current(self):
        return self.STATES.get(f'ID{self.chat_id}').get('state')