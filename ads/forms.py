from django.core.exceptions import ValidationError
from django import forms
from .models import Ad, ExchangeProposal
from django.db.models import Q


class NewAdForm(forms.ModelForm):
    class Meta:
        model = Ad
        exclude = ["user"]

class NewExchangeProposalForm(forms.ModelForm):
    comment = forms.CharField(max_length=500, widget=forms.Textarea(attrs={"rows": 3}))

    class Meta:
        model = ExchangeProposal
        fields = ["ad_sender", "ad_receiver", "comment"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["ad_sender"].queryset = Ad.objects.filter(user=self.user)
        self.fields["ad_receiver"].queryset = Ad.objects.filter(~Q(user=self.user))

    def clean_ad_sender(self):
        ad_sender = self.cleaned_data["ad_sender"]
        if ad_sender.user != self.user:
            list_of_allowed_ads = Ad.objects.filter(user=self.user).all()
            if list_of_allowed_ads:
                raise ValidationError(
                    "Этот товар вам не принадлежит. Список доступных товаров: " + ", ".join(
                        [f"{i_ad.id} - {i_ad.title}" for i_ad in list_of_allowed_ads]
                    )
                )
        return ad_sender

    def clean_ad_receiver(self):
        ad_receiver = self.cleaned_data["ad_receiver"]
        if ad_receiver.user == self.user:
            raise ValidationError("Нельзя обмениваться на свои товары.")
        return ad_receiver
