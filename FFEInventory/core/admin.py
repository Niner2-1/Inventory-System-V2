from django.contrib import admin
from django.urls.resolvers import URLPattern
from .models import *


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = [
        "FFE_number",
        "old_FFE",
        "item_type",
        "processor",
        "motherboard",
        "memory",
        "video_card",
        "hard_disk",
        "others",
        "description",
        "cost",
        "date_purchased",
        "originating_branch",
        "current_branch",
        "status",
        "custody",
    ]
    exclude = ["is_deleted"]
    list_filter = ("current_branch__name", "item_type")
    search_fields = ["FFE_number"]

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name="encoder").exists():
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name="encoder").exists():
            return False
        return super().has_delete_permission(request, obj)


admin.site.register(Transaction)
admin.site.register(Custody)
admin.site.register(Branch)
