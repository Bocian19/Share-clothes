from django.contrib import admin
from .models import Institution, Donation, Category
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.


admin.site.register(Category)


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'type')
    list_display_links = ('type',)
    list_filter = ('type',)


def telephone(obj):
    return f"+48 {obj.phone_number}"


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    empty_value_display = 'Empty'
    fields = ('quantity', 'institution','category', 'address', telephone,
                    'city', ('pick_up_date', 'pick_up_time'), 'pick_up_comment',
                    'user', 'is_taken', 'date_updated')
    exclude = ('date_updated',)

    def category(self, obj):
        return ",".join([str(i) for i in obj.categories.all()])


admin.site.unregister(User)
admin.site.disable_action('delete_selected')

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # pass
    actions = ['delete_queryset']

    def delete_queryset(self, request, queryset):
        if User.objects.all().filter(is_superuser=True).count() > queryset.filter(is_superuser=True).count():
            queryset.delete()
            self.message_user(request, 'Usunięto wybranych użytkowników')
        else:
            self.message_user(request, 'Nie możesz usunąć jedynego superusera')
    delete_queryset.short_description = 'Usuń wybranych użytkowników-custom'



