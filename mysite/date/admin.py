from django.contrib import admin
from date.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'first_name', 'last_name', 'email', 'photo', 'gender')
    list_filter = ('gender',)
    list_editable = ('gender',)
    search_fields = ('first_name', 'last_name', 'email')


admin.site.register(User, UserAdmin)
