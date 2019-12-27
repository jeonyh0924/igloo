from django.contrib import admin
from posts.models import *

# Register your models here.
admin.site.register(Posts)
admin.site.register(Postlikes)
admin.site.register(Comments)
admin.site.register(HousingTypes)
admin.site.register(Styles)
admin.site.register(Colors)
admin.site.register(Images)
