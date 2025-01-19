from django.contrib import admin

from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email','username', 'allowed_to_add')
    list_editable = ('allowed_to_add',)