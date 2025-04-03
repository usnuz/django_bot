from typing import Optional


class StateManager:

    STATES = {}

    def __init__(self, chat_id, user_id):
        self.chat_id = chat_id,
        self.user_id = user_id
        self.STATES[f'ID{self.chat_id}|{self.user_id}'] = {}

    def set(self, name):
        self.STATES[f'ID{self.chat_id}|{self.user_id}'].update({'state': name})

    def update(self, data: dict) -> None:
        self.STATES[f'ID{self.chat_id}|{self.user_id}'].update({'data': data})

    def get(self):
        return self.STATES.get(f'ID{self.chat_id}|{self.user_id}')

    def clear(self):
        del self.STATES[f'ID{self.chat_id}|{self.user_id}']

    def current(self):
        self.STATES.get(f'ID{self.chat_id}|{self.user_id}').get('state')