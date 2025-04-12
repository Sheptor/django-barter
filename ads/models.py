from django.db import models
from django.contrib.auth.models import User


class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Заголовок объявления")
    description = models.CharField(max_length=500, verbose_name="Описание товара")
    image_url = models.URLField(blank=True, null=True, verbose_name="URL изображения")
    category = models.CharField(max_length=200, verbose_name="Категория товара")
    condition = models.CharField(max_length=200, verbose_name="Состояние товара")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    def __str__(self):
        return f"{self.title}"


class ExchangeProposal(models.Model):
    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="sender", default="", verbose_name="Ваш товар")
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="receiver", default="", verbose_name="Обменять на")
    comment = models.CharField(max_length=500, verbose_name="Комментарий", default="")
    status = models.CharField(choices=[
        ("waiting", "ожидает"), ("accepted", "принята"), ("rejected", "отклонена")
    ], default="ожидает", verbose_name="Статус предложения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации предложения")

    def __str__(self):
        return f"{self.ad_sender} - {self.ad_receiver}"
