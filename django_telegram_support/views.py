from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .forms import SupportForm
from .telegram import send_message
from .conf import THROTTLE_SECONDS, SOURCE

def _throttle_key(request):
    ip = request.META.get("REMOTE_ADDR", "unknown")
    return f"tg_support_throttle:{ip}"

@require_http_methods(["GET", "POST"])
def support_view(request, template_name="django_telegram_support/support_form.html", success_redirect_name=None):
    if request.method == "POST":
        form = SupportForm(request.POST)
        if form.is_valid():
            key = _throttle_key(request)
            if cache.get(key):
                messages.error(request, "Please wait a minute before sending another message.")
                return redirect(request.path)
            cache.set(key, timezone.now().timestamp(), THROTTLE_SECONDS)

            email = form.cleaned_data["email"].strip()
            body = form.cleaned_data["message"].strip()

            header = f"*Support ({SOURCE})*\n*Email:* {email}\n\n*Message:*\n"
            remaining = 4096 - len(header)
            text = header + body[: max(0, remaining)]

            if send_message(text):
                messages.success(request, "Thanks! Your message has been sent.")
                return redirect(request.path if not success_redirect_name else success_redirect_name)
            messages.error(request, "Could not send your message. Please try again later.")
    else:
        form = SupportForm()
    return render(request, template_name, {"form": form})
