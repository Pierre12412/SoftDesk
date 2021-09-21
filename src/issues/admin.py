from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from issues.models import User

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff',)
    search_fields = ('first_name', 'last_name', 'email')
    fields = ('first_name','last_name','email','password','is_active','is_staff','is_admin')

admin.site.register(User, CustomUserAdmin)