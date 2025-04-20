import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect

from .forms import NewAdForm, NewExchangeProposalForm
from .models import Ad, ExchangeProposal


class HomeView(generic.TemplateView):
    template_name = "ads/index.html"


class AllAddsView(generic.ListView):
    page_pattern = re.compile(r"page=\d+&?")
    template_name = "ads/ads_list.html"
    context_object_name = "ads"
    paginate_by = 15

    def get_queryset(self):
        ads_queryset = Ad.objects.all()

        category = self.request.GET.get("category")
        if category:
            ads_queryset = ads_queryset.filter(category=category)

        condition = self.request.GET.get("condition")
        if condition:
            ads_queryset = ads_queryset.filter(condition=condition)

        ordering = self.request.GET.get("ordering", "-created_at")
        if ordering in {"created_at", "-created_at", "title", "-title"}:
            ads_queryset = ads_queryset.order_by(ordering)

        search = self.request.GET.get("search")
        if search:
            ads_queryset = ads_queryset.filter(
                Q(title__contains=search) |
                Q(category__contains=search) |
                Q(description__contains=search)
            )

        return ads_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories_list"] = Ad.objects.values_list("category", flat=True).distinct()
        context["conditions_list"] = Ad.objects.values_list("condition", flat=True).distinct()
        query_params = self.request.GET.urlencode()
        query_params = re.sub(self.page_pattern, "", query_params)
        context["current_params"] = query_params
        return context


class CreateAdView(LoginRequiredMixin, generic.CreateView):
    model = Ad
    form_class = NewAdForm
    template_name = "ads/ad_form.html"

    def form_valid(self, form):
        self.request.session["tmp_ad_data"] = form.cleaned_data
        return redirect("ads:ad_confirmation")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("users:login")
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        tmp_ad_data = self.request.session.get("tmp_ad_data")
        if tmp_ad_data:
            for i_key, i_value in tmp_ad_data.items():
                initial[i_key] = i_value
        return initial


class AdConfirmationView(LoginRequiredMixin, generic.CreateView):
    model = Ad
    template_name = "ads/ad_detail.html"
    form_class = NewAdForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tmp_ad_data = self.request.session.get("tmp_ad_data")
        if not tmp_ad_data:
            raise PermissionDenied("Данные не найдены")
        tmp_ad = Ad(user=self.request.user, **tmp_ad_data)
        tmp_ad.id = "___"
        context["ad"] = tmp_ad
        context["is_owner"] = tmp_ad.user == self.request.user
        context["is_confirmation"] = True
        return context

    def post(self, request, *args, **kwargs):
        tmp_ad_data = request.session.get("tmp_ad_data")
        if not tmp_ad_data:
            return redirect("ads:new_ad")
        ad = Ad.objects.create(user=request.user, **tmp_ad_data)
        return redirect("ads:ad_detail", pk=ad.id)


class AdDetailView(generic.DetailView):
    model = Ad
    template_name = "ads/ad_detail.html"
    context_object_name = "ad"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_have_ads"] = Ad.objects.filter(user=self.request.user).exists()
        context["is_owner"] = self.object.user == self.request.user
        context["is_confirmation"] = False

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_owner"] = self.object.user == self.request.user
        context["is_confirmation"] = False
        context["is_edit"] = True
        return context

    def get_success_url(self):
        return reverse_lazy("ads:ad_detail", kwargs={"pk": self.object.id})


class AdDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ad
    template_name = "ads/ad_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_delete"] = True
        context["is_owner"] = self.object.user == self.request.user
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
    template_name = "ads/exchange_list.html"
    context_object_name = "exchanges_list"
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_have_exchanges"] = Ad.objects.filter(user=self.request.user).exists()

        return context

    def get_queryset(self):
        return ExchangeProposal.objects.filter(Q(ad_sender__user=self.request.user) | Q(ad_receiver__user=self.request.user)).all()


class CreateExchangeProposalView(LoginRequiredMixin, generic.CreateView):
    model = ExchangeProposal
    form_class = NewExchangeProposalForm
    template_name = "ads/exchange_form.html"

    def get_initial(self):
        initial = super().get_initial()
        ad_id = self.kwargs.get("ad_id")

        if ad_id:
            initial["ad_receiver"] = ad_id
        return initial

    def form_valid(self, form):
        self.request.session["tmp_exchange_data"] = form.cleaned_data
        self.request.session["tmp_exchange_data"]["ad_sender"] = form.cleaned_data["ad_sender"].id
        self.request.session["tmp_exchange_data"]["ad_receiver"] = form.cleaned_data["ad_receiver"].id
        return redirect("ads:exchange_confirmation")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("users:login")
        else:
            return super().dispatch(request, *args, **kwargs)


class ExchangeProposalConfirmationView(LoginRequiredMixin, generic.CreateView):
    model = ExchangeProposal
    template_name = "ads/exchange_detail.html"
    form_class = NewExchangeProposalForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tmp_exchange_data = self.request.session.get("tmp_exchange_data")
        if not tmp_exchange_data:
            raise PermissionDenied("Данные не найдены")
        tmp_exchange_data["ad_sender"] = Ad.objects.get(pk=tmp_exchange_data["ad_sender"])
        tmp_exchange_data["ad_receiver"] = Ad.objects.get(pk=tmp_exchange_data["ad_receiver"])
        tmp_exchange = ExchangeProposal(**tmp_exchange_data)
        tmp_exchange.id = "___"
        tmp_exchange.created_at = "_" * 15
        context["exchange_proposal"] = tmp_exchange
        context["is_owner"] = tmp_exchange.ad_sender.user == self.request.user
        context["is_confirmation"] = True
        return context

    def post(self, request, *args, **kwargs):
        tmp_exchange_data = request.session.get("tmp_exchange_data")
        if not tmp_exchange_data:
            return redirect("ads:new_exchange")
        tmp_exchange_data["ad_sender"] = Ad.objects.get(pk=tmp_exchange_data["ad_sender"])
        tmp_exchange_data["ad_receiver"] = Ad.objects.get(pk=tmp_exchange_data["ad_receiver"])
        exchange = ExchangeProposal.objects.create(**tmp_exchange_data)
        return redirect("ads:exchange_detail", pk=exchange.id)



class ExchangeProposalDetailView(LoginRequiredMixin, generic.DetailView):
    model = ExchangeProposal
    template_name = "ads/exchange_detail.html"
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

    def post(self, request, *args, **kwargs):
        exchange = self.get_object()
        if request.user == exchange.ad_receiver.user:
            action = request.POST.get("set-status-button", None)
            if action == "accept":
                exchange.set_status("accepted")
            elif action == "reject":
                exchange.set_status("rejected")
            elif action == "recreate":
                exchange.ad_sender, exchange.ad_receiver = exchange.ad_receiver, exchange.ad_sender
                exchange.set_status("waiting")
            return HttpResponseRedirect(reverse_lazy("ads:exchange_detail", kwargs={"pk": exchange.id}))
        else:
            raise PermissionDenied("Только получатель может изменять статус предложения")


class ExchangeProposalEditView(LoginRequiredMixin, generic.UpdateView):
    model = ExchangeProposal
    form_class = NewExchangeProposalForm
    template_name = "ads/exchange_form.html"
    context_object_name = "exchange_proposal"

    def get_success_url(self):
        return reverse_lazy("ads:exchange_detail", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_owner"] = self.object.ad_sender.user == self.request.user
        context["is_edit"] = True
        return context

    def get_object(self, queryset=None):
        exchange = get_object_or_404(ExchangeProposal, pk=self.kwargs.get("pk"))
        if exchange.ad_sender.user != self.request.user:
            raise PermissionDenied("У вас нет прав для изменения владельца объявления")
        return exchange



class ExchangeProposalDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ExchangeProposal
    template_name = "ads/exchange_detail.html"
    context_object_name = "exchange_proposal"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_owner"] = self.object.ad_sender.user == self.request.user
        context["is_delete"] = True
        return context

    def get_object(self, queryset=None):
        exchange = get_object_or_404(ExchangeProposal, pk=self.kwargs.get("pk"))
        if exchange.ad_sender.user != self.request.user:
            raise PermissionDenied("У вас не достаточно прав для изменения объявления")
        return exchange

    def get_success_url(self):
        return reverse_lazy("ads:exchanges")
