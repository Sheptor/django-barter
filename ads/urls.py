from django.urls import path

from . import views

app_name = "ads"
urlpatterns = [
    path("", views.AllAddsView.as_view(), name="ads"),
    path("new_ad/", views.CreateAdView.as_view(), name="new_ad"),
    path("<int:pk>/", views.AdDetailView.as_view(), name="ad_detail"),
    path("edit/<int:pk>/", views.AdEditView.as_view(), name="ad_edit"),
    path("delete/<int:pk>/", views.AdDeleteView.as_view(), name="ad_delete"),
    path("exchange/", views.ExchangeProposalListView.as_view(), name="exchanges"),
    path("exchange/<int:pk>/", views.ExchangeProposalDetailView.as_view(), name="exchange_detail"),
    path("exchange/new/<int:ad_id>", views.CreateExchangeProposalView.as_view(), name="new_exchange"),
    path("exchange/new/", views.CreateExchangeProposalView.as_view(), name="new_exchange"),
    path("exchange/edit/<int:pk>/", views.CreateExchangeProposalView.as_view(), name="exchange_edit"),
    path("exchange/delete/<int:pk>/", views.ExchangeProposalDeleteView.as_view(), name="exchange_delete"),
]
