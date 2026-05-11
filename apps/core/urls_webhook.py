from django.urls import path

from apps.core import webhook

urlpatterns = [
    path("webhook/", webhook.github_webhook, name="github_webhook"),
]
