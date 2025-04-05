from django.urls import path

from . import views

app_name = "ads"
urlpatterns = [
    path("", views.AllAddsView.as_view(), name="ads"),
    path("<int:pk>/", views.AdDetailView.as_view(), name="ad_detail"),
    path("<int:pk>/new_ad", views.Reg.as_view(), name="new_ad"),
]
