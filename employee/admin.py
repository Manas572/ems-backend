from django.contrib import admin
from .models import User, Employee

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "role")
    ordering = ("email",)

admin.site.register(Employee)