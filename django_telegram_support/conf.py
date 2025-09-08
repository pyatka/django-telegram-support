from django.conf import settings

BOT_TOKEN = getattr(settings, "TELEGRAM_BOT_TOKEN", None)
CHAT_ID = getattr(settings, "TELEGRAM_CHAT_ID", None)
SOURCE = getattr(settings, "TELEGRAM_SOURCE", "unknown-project")

MAX_MESSAGE_LEN = getattr(settings, "TELEGRAM_SUPPORT_MAX_MESSAGE_LEN", 3500)
THROTTLE_SECONDS = getattr(settings, "TELEGRAM_SUPPORT_THROTTLE_SECONDS", 60)