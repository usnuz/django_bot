import json
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from .models import TelegramBot


logger = logging.getLogger(__name__)

@csrf_exempt
def telegram_webhook(request, pk):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            bot = TelegramBot.objects.get(id=pk)
            bot.dp.updater(data)
            return JsonResponse({"status": "success"}, status=200)
        except Exception as e:
            logger.error(f"Error in webhook: {str(e)}")
            return JsonResponse({"status": "failed", "message": str(e)}, status=400)
    return JsonResponse({"status": "ok"}, status=200)


def get_webhook(request):
    bots = TelegramBot.objects.all()
    ws = []
    for bot in bots:
        ws.append(f'{request.build_absolute_uri()}{bot.id}')
    return JsonResponse({"status": "ok", "webhooks": ws}, status=200)


