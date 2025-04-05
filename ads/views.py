from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Ad


class AllAddsView(generic.ListView):
    template_name = "ads/index.html"
    context_object_name = "ads"

    def get_queryset(self):
        return Ad.objects.all()


class AdDetailView(generic.DetailView):
    model = Ad
    template_name = "ads/ad_detail.html"
    context_object_name = "ad"

    def get_object(self):
        pk=self.kwargs.get("pk")
        ad = get_object_or_404(Ad, pk=pk)
        return ad


class Reg(generic.CreateView):
    model = Ad
    fields = ["title", "description", "category", "condition"]