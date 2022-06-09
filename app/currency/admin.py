from currency.models import Source

from django.contrib import admin


class SourceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'code_name',
        'url',
    )


admin.site.register(Source, SourceAdmin)
