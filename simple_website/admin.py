from django.contrib import admin
from .models import MakePost

class MakePostAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(MakePost, MakePostAdmin)
