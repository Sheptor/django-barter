from django.core.exceptions import ValidationError
from django import forms
from .models import Ad, ExchangeProposal


class NewAdForm(forms.ModelForm):
    class Meta:
        model = Ad
        exclude = ["user"]

class NewExchangeProposalForm(forms.ModelForm):
    ad_sender = forms.IntegerField(min_value=1)
    ad_receiver = forms.IntegerField(min_value=1)
    comment = forms.CharField(max_length=500, widget=forms.Textarea(attrs={"rows": 3}))

    class Meta:
        model = ExchangeProposal
        fields = ["ad_sender", "ad_receiver", "comment"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_ad_sender(self):
        try:
            ad_sender = Ad.objects.get(pk=self.cleaned_data["ad_sender"])
        except Ad.DoesNotExist:
            raise ValidationError("Товара не существует.")
        if ad_sender.user != self.user:
            list_of_allowed_ads = Ad.objects.filter(user=self.user).all()
            if list_of_allowed_ads:
                raise ValidationError(
                    "Этот товар вам не принадлежит. Список доступных товаров: " + ", ".join(
                        [str(i_ad.id) for i_ad in list_of_allowed_ads]
                    )
                )
        return ad_sender

    def clean_ad_receiver(self):
        try:
            ad_receiver = Ad.objects.get(pk=self.cleaned_data["ad_receiver"])
        except Ad.DoesNotExist:
            raise ValidationError("Товара не существует.")
        if ad_receiver.user == self.user:
            raise ValidationError("Нельзя обмениваться на свои товары.")
        return ad_receiver

    def clean(self):
        try:
            ad_sender = self.cleaned_data["ad_sender"]
            ad_receiver = self.cleaned_data["ad_receiver"]
        except KeyError:
            raise ValidationError("Ошибка полей")
        try:
            exchange = ExchangeProposal.objects.get(ad_sender=ad_sender.id, ad_receiver=ad_receiver.id)
        except ExchangeProposal.DoesNotExist:
            try:
                exchange = ExchangeProposal.objects.get(ad_sender=ad_receiver.id, ad_receiver=ad_sender.id)
            except ExchangeProposal.DoesNotExist:
                return

        if exchange.status != "rejected":
            self.errors["ad_sender"] = f"Предложение обмена {ad_sender.id} на {ad_receiver.id} уже {exchange.status}"
            raise ValidationError("Ошибка полей")
