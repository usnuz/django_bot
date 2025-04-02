import requests

from django.db import models
from bot.router import Router

from types import SimpleNamespace



class TelegramBot(models.Model):

    DISPATCHERS = {}

    id = models.BigIntegerField(unique=True, primary_key=True)
    token = models.CharField(max_length=255, unique=True)
    base_api = models.URLField(default='https://api.telegram.org/')
    parse_mode = models.CharField(max_length=255, default='HTML')

    @property
    def api(self):
        return f'{self.base_api}bot{self.token}/'

    @property
    def dp(self):
        if str(self.id) in self.DISPATCHERS:
            return self.DISPATCHERS[self.id]
        else:
            dispatcher = Router(self)
            self.DISPATCHERS[str(self.id)] = dispatcher
            return dispatcher

    def send_message(self, chat_id, text, reply_markup=None):
        data = {'chat_id': chat_id, 'text': text}
        if reply_markup:
            data['reply_markup'] = reply_markup
        return self._post('sendMessage', json=data)

    def send_photo(self, chat_id, buffer, caption=None, reply_markup=None):
        data = {'chat_id': chat_id}
        if caption:
            data['caption'] = caption
        if reply_markup:
            data['reply_markup'] = reply_markup
        files = {'photo': ('image.jpg', buffer , "image/jpeg")}
        return self._post('sendPhoto', json=data, files=files)

    def _post(self, method, json=None, files=None):
        if json is not None:
            json['parse_mode'] = self.parse_mode
        result = requests.post(self.api + method, json=json, files=files)
        return SimpleNamespace(**result.json())

















