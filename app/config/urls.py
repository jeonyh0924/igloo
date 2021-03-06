"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from members.urls import urlpatterns_api_members
from members.views import facebook_login_page
from posts.urls import urlpatterns_api_posts

urlpatterns_api = ([
                       path('members/', include(urlpatterns_api_members)),
                       path('posts/', include(urlpatterns_api_posts)),
                   ], 'api')
urlpatterns = [
    path('api/token/', obtain_jwt_token),  # jwt Token get it
    path('api/token/refresh/', refresh_jwt_token),  # jwt Token refresh
    path('api/token/verify/', verify_jwt_token),  # jwt Token verify
    path('admin/', admin.site.urls),
    path('api/', include(urlpatterns_api)),
    path('login/', facebook_login_page, name='login-page'),
    path('members/', include(urlpatterns_api_members)),
]

urlpatterns += static(
    prefix=settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
