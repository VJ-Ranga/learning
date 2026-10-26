from django.contrib import admin
from .models import Attempt

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'mission_slug', 'score', 'passed', 'created_at')
    list_filter = ('mission_slug', 'passed')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)
