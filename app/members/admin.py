from django.contrib import admin
from .models import Users, Relations


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    search_fields = ('username', )


admin.site.register(Users, UserAdmin)
admin.site.register(Relations)
