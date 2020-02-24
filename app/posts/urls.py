from django.urls import path

from . import apis

urlpatterns_api_posts = [
    path('', apis.PostsListCreateView.as_view()),
    path('postDetail/<int:pk>/', apis.PostDetail.as_view()),
    path('postLike/<int:post_pk>/', apis.PostLikeView.as_view()),
    path('commentCreate/<int:post_pk>/', apis.CommentView.as_view()),
    path('commentUpdateDelete/<int:pk>/', apis.CommentUpdateDelete.as_view()),
    path('postFiltering/', apis.PostFiltering.as_view()),
]
