from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Profile


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'id', 'date_joined', 'username', 'email', 'is_active', 'is_staff', 'is_superuser',
        'provider_list', 'first_name', 'last_name',
    )
    list_filter = (
        ('date_joined', admin.DateFieldListFilter),
        'is_active', 'is_staff', 'is_superuser',
    )
    list_editable = ('is_active', 'is_staff', 'is_superuser', 'first_name', 'last_name',)
    search_fields = ('username', 'email', 'first_name', 'last_name',)

    class Meta:
        ordering = ('-date_joined', 'username',)

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).prefetch_related('socialaccount_set')

    def provider_list(self, obj):
        return ", ".join([sa.provider for sa in obj.socialaccount_set.all()])


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name')
    list_editable = ('name',)
