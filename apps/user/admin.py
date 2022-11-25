from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User  # pylint: disable=imported-auth-user
from django.db.models import QuerySet
from django.http import HttpRequest

from import_export.admin import ImportExportMixin

from .models import Profile


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class CustomUserAdmin(ImportExportMixin, UserAdmin):
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


class EmailVerifiedListFilter(admin.SimpleListFilter):
    title = 'email verified'
    parameter_name = 'email_verified_on'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(email_verified_on__isnull=False)
        if self.value() == 'no':
            return queryset.filter(email_verified_on__isnull=True)
        return queryset


@admin.register(Profile)
class ProfileAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('user',)
