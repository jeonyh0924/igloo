from django.urls import path

from posts import apis

urlpatterns_api_posts = [
    path('postList/', apis.PostList.as_view()),
    path('postDetail/<int:pk>/', apis.PostDetail.as_view()),
]
