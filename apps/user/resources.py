from import_export import resources
from import_export.fields import Field

from .models import Profile


class ProfileResource(resources.ModelResource):
    username = Field(attribute='username')
    email = Field(attribute='email')
    active = Field(attribute='active')
    account_type = Field(column_name='account type')
    num_entries = Field(attribute='num_entries', column_name='# entries')
    num_bullets = Field(attribute='num_bullets', column_name='# bullets')
    latest_entry_date = Field(attribute='latest_entry_date', column_name='last entry date')
    num_dreams = Field(attribute='num_dreams')
    num_gems = Field(attribute='num_gems')
    num_ideas = Field(attribute='num_ideas')
    day_ends_at = Field()
    dreams_enabled = Field(attribute='dreams_enabled')
    notes_enabled = Field(attribute='notes_enabled')
    gems_enabled = Field(attribute='gems_enabled')
    ideas_enabled = Field(attribute='ideas_enabled')

    class Meta:
        model = Profile
        fields = (
            'id', 'created_sts', 'username', 'email', 'active', 'account_type',
            'email_verified_on', 'num_entries', 'num_bullets', 'latest_entry_date',
            'num_dreams', 'num_gems', 'num_ideas', 'birthday', 'day_ends_at',
            'dreams_enabled', 'gems_enabled', 'ideas_enabled',
        )
        export_order = (
            'id', 'created_sts', 'username', 'email', 'active', 'email_verified_on',
            'account_type', 'num_entries', 'num_bullets', 'latest_entry_date',
            'num_dreams', 'num_gems', 'num_ideas', 'birthday', 'day_ends_at',
            'dreams_enabled', 'gems_enabled', 'ideas_enabled',
        )

    def dehydrate_account_type(self, obj: Profile) -> str:
        return obj.get_account_type_display()

    def dehydrate_day_ends_at(self, obj: Profile) -> str:
        return f'{obj.day_ends_at} AM'
