from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Q

from .forms import NewAdForm, NewExchangeProposalForm
from .models import Ad, ExchangeProposal


class HomeView(generic.TemplateView):
    template_name = "ads/index.html"


class AllAddsView(generic.ListView):
    template_name = "ads/ads_list.html"
    context_object_name = "ads"
    paginate_by = 15

    def get_queryset(self):
        return Ad.objects.all()


class CreateAdView(LoginRequiredMixin, generic.CreateView):
    model = Ad
    form_class = NewAdForm
    template_name = "ads/ad_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateAdView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("users:login")
        else:
            return super(CreateAdView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("ads:ad_detail", kwargs={"pk": self.object.id})


class AdDetailView(generic.DetailView):
    model = Ad
    template_name = "ads/ad_detail.html"
    context_object_name = "ad"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_have_ads"] = Ad.objects.filter(user=self.request.user).exists()
        context["is_owner"] = self.object.user == self.request.user

        return context

    def get_object(self):
        pk=self.kwargs.get("pk")
        ad = get_object_or_404(Ad, pk=pk)
        return ad


class AdEditView(LoginRequiredMixin, generic.UpdateView):
    model = Ad
    template_name = "ads/ad_form.html"
    form_class = NewAdForm

    def get_object(self, queryset=None):
        ad = get_object_or_404(Ad, pk=self.kwargs.get("pk"))
        if ad.user != self.request.user:
            raise PermissionDenied("У вас нет прав для изменения владельца объявления")
        return ad

    def get_success_url(self):
        return reverse_lazy("ads:ad_detail", kwargs={"pk": self.object.id})


class AdDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ad
    template_name = "ads/ad_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_delete"] = True
        return context

    def get_object(self, queryset=None):
        ad = get_object_or_404(Ad, pk=self.kwargs.get("pk"))
        if ad.user != self.request.user:
            raise PermissionDenied("У вас нет прав для изменения владельца объявления")
        return ad

    def get_success_url(self):
        return reverse_lazy("ads:ads")


class ExchangeProposalListView(LoginRequiredMixin, generic.ListView):
    model = ExchangeProposal
    template_name = "ads/exchange_proposal_list.html"
    context_object_name = "exchanges_list"
    paginate_by = 15

    def get_queryset(self):
        return ExchangeProposal.objects.filter(Q(ad_sender__user=self.request.user) | Q(ad_receiver__user=self.request.user)).all()


class CreateExchangeProposalView(LoginRequiredMixin, generic.CreateView):
    model = ExchangeProposal
    form_class = NewExchangeProposalForm
    template_name = "ads/exchange_proposal_form.html"

    def get_initial(self):
        initial = super().get_initial()
        ad_id = self.kwargs.get("ad_id")

        if ad_id:
            initial["ad_receiver"] = get_object_or_404(Ad, id=ad_id)
        return initial

    def form_valid(self, form):
        return super(CreateExchangeProposalView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("users:login")
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("ads:exchange_proposal_detail", kwargs={"pk": self.object.id})


class ExchangeProposalDetailView(LoginRequiredMixin, generic.DetailView):
    model = ExchangeProposal
    template_name = "ads/exchange_proposal_detail.html"
    context_object_name = "exchange_proposal"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_owner"] = self.object.ad_sender.user == self.request.user
        context["is_delete"] = False
        return context

    def get_object(self, queryset=None):
        exchange = super().get_object(queryset=queryset)

        current_user = self.request.user
        is_owner = (exchange.ad_sender.user == current_user)
        is_receiver = (exchange.ad_receiver.user == current_user)

        if not (is_owner or is_receiver):
            raise PermissionDenied("У вас нет прав для просмотра этого предложения")

        return exchange


class ExchangeProposalEditView(LoginRequiredMixin, generic.UpdateView):
    model = ExchangeProposal
    form_class = NewExchangeProposalForm
    template_name = "ads/exchange_proposal_form.html"
    context_object_name = "exchange_proposal"

    def get_success_url(self):
        return reverse_lazy("ads:exchange_proposal_detail", kwargs={"pk": self.object.id})

    def get_object(self, queryset=None):
        exchange = get_object_or_404(ExchangeProposal, pk=self.kwargs.get("pk"))
        if exchange.ad_sender.user != self.request.user:
            raise PermissionDenied("У вас нет прав для изменения владельца объявления")
        return exchange


class ExchangeProposalDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ExchangeProposal
    template_name = "ads/exchange_proposal_detail.html"
    context_object_name = "exchange_proposal"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_owner"] = self.object.ad_sender.user == self.request.user
        context["is_delete"] = True
        return context

    def get_object(self, queryset=None):
        exchange = get_object_or_404(ExchangeProposal, pk=self.kwargs.get("pk"))
        if exchange.ad_sender.user != self.request.user:
            raise PermissionDenied("У вас нет прав для изменения владельца объявления")
        return exchange

    def get_success_url(self):
        return reverse_lazy("ads:exchanges")
