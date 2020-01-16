from django.urls import path

from posts import apis

urlpatterns_api_posts = [
    path('postsView/', apis.PostsView.as_view()),
    path('postDetail/<int:pk>/', apis.PostDetail.as_view()),
]
