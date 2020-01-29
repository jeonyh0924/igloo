from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'title',
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'author',

    )


# Register your models here.
admin.site.register(Posts, PostAdmin)
admin.site.register(PostLike)
admin.site.register(Comments, CommentAdmin)
admin.site.register(HousingTypes)
admin.site.register(Styles)
admin.site.register(Colors)
admin.site.register(PostImages)
