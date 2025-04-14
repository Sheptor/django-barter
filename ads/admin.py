from django.contrib import admin
from .models import Ad, ExchangeProposal

class AdInLine(admin.TabularInline):
    model = Ad
    extra = 3
    fields = ["user", "title", "created_at"]


class ExchangeProposalAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None, {"fields": ["Sender user", "Receiver user", "Sender ad", "Receiver ad"]}),
    #     ("Date information", {"fields": ["created_at"]})
    # ]
    list_display = ["ad_sender", "ad_receiver", "created_at"]
    list_filter = ["created_at"]
    readonly_fields = ["created_at"]
    search_fields = ["ad_sender", "ad_receiver"]
    can_edit = True

admin.site.register(Ad)
admin.site.register(ExchangeProposal, ExchangeProposalAdmin)
