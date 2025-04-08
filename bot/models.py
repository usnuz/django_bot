import aiohttp
import asyncio
import requests
import time

from django.db import models
from bot.router import Router

from .types import TelegramObject

from asgiref.sync import sync_to_async



class TelegramBot(models.Model):

    DISPATCHERS = {}

    token = models.CharField(max_length=255, unique=True)
    base_api = models.URLField(default='https://api.telegram.org/')
    parse_mode = models.CharField(max_length=255, default='HTML')
    offset = models.BigIntegerField(default=0)

    @property
    def api(self):
        return f'{self.base_api}bot{self.token}/'

    @property
    def dp(self):
        if str(self.token) in self.DISPATCHERS:
            return self.DISPATCHERS[self.token]
        else:
            dispatcher = Router(self)
            self.DISPATCHERS[str(self.token)] = dispatcher
            return dispatcher

    @classmethod
    def set(cls, token):
        bot = TelegramBot.objects.filter(token=token).first()
        if bot:
            return bot
        else:
            bot = TelegramBot.objects.create(token=token)
            return bot

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

    def edit_message_reply_markup(self, chat_id, message_id, reply_markup=None):
        data = {"chat_id": chat_id, "message_id": message_id, reply_markup: reply_markup}
        return self._post('editMessageReplyMarkup', json=data)

    def delete_message(self, chat_id, message_id):
        data = {"chat_id": chat_id, "message_id": message_id}
        return self._post('deleteMessage', json=data)

    def delete_messages(self, chat_id, message_ids):
        data = {"chat_id": chat_id, "message_ids": message_ids}
        return self._post('deleteMessages', json=data)

    def answer_callback_query(self, callback_query_id, text, show_alert=False):
        data = {'callback_query_id': callback_query_id, 'text': text, 'show_alert': show_alert}
        return self._post('answerCallbackQuery', json=data)

    def _post(self, method, json=None, files=None):
        if json is not None:
            json['parse_mode'] = self.parse_mode
        result = requests.post(self.api + method, json=json, files=files)
        return TelegramObject(result.json())

    def _start_polling(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.polling_loop())

    async def polling_loop(self):
        async with aiohttp.ClientSession() as session:
            while True:
                updates = await self._get_updates(session)
                if updates.get('ok'):
                    results = updates.get('result', [])
                    if results:
                        print(results)
                        last_update = results[-1]
                        self.offset = last_update['update_id'] + 1
                        await sync_to_async(self.save, thread_sensitive=True)(update_fields=['offset'])
                        self.dp.updater(last_update)
                await asyncio.sleep(1)

    async def __get_updates(self, session):
        url = self.api + 'getUpdates'
        params = {'offset': self.offset} if self.offset else {}
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            return {}

    def start_polling(self):
        while True:
            updates = self._get_updates()
            if updates.get('ok'):
                results = updates.get('result', [])
                if results:
                    print(results)
                    last_update = results[-1]
                    self.offset = last_update['update_id'] + 1
                    self.save(update_fields=['offset'])
                    self.dp.updater(last_update)
            time.sleep(1)

    def _get_updates(self):
        url = self.api + 'getUpdates'
        params = {'offset': self.offset} if self.offset else {}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return {}

















