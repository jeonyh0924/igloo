from django.urls import path

from . import apis

urlpatterns_api_posts = [
    path('postsView/', apis.PostsView.as_view()),
    path('postDetail/<int:pk>/', apis.PostDetail.as_view()),
    path('postLikeCreate/<int:post_pk>/', apis.PostLikeCreate.as_view()),
    path('commentView/<int:post_pk>/', apis.CommentView.as_view()),


]

