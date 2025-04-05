from django.db import models
from django import forms
from django.contrib.auth.models import User


class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=200)
    condition = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class ExchangeProposal(models.Model):
    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="sender", default="")
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="receiver", default="")
    comment = models.CharField(max_length=500)
    status = models.CharField(choices=[
        ("waiting", "ожидает"), ("accepted", "принята"), ("rejected", "отклонена")
    ], default="ожидает")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ad_sender} - {self.ad_receiver}"
