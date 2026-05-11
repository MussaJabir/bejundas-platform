import hashlib
import hmac
import logging
import os
import subprocess

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def github_webhook(request):
    secret = getattr(settings, "GITHUB_WEBHOOK_SECRET", "").encode()
    if not secret:
        logger.error("GITHUB_WEBHOOK_SECRET not set")
        return HttpResponseForbidden("Not configured")

    signature_header = request.META.get("HTTP_X_HUB_SIGNATURE_256", "")
    if not signature_header.startswith("sha256="):
        return HttpResponseForbidden("Invalid signature format")

    expected = hmac.new(secret, request.body, hashlib.sha256).hexdigest()
    received = signature_header[len("sha256=") :]

    if not hmac.compare_digest(expected, received):
        logger.warning("Webhook signature mismatch")
        return HttpResponseForbidden("Invalid signature")

    script = os.path.join(settings.BASE_DIR, "scripts", "deploy.sh")
    subprocess.Popen(
        ["bash", script],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=True,
        start_new_session=True,
    )
    logger.info("Deploy script triggered")
    return HttpResponse("OK", status=200)
