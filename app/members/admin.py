from django.contrib import admin
from .models import Users, Relations


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    search_fields = ('id', 'username',)


class RelationAdmin(admin.ModelAdmin):
    list_display = (
        'from_user',
        'to_user',
        'related_type',
        'created_at',
    )


admin.site.register(Users, UserAdmin)
admin.site.register(Relations, RelationAdmin)
