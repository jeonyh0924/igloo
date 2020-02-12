from django.urls import path

from . import apis

urlpatterns_api_posts = [
    path('postCreate/', apis.PostsCreateView.as_view()),
    path('postList/', apis.PostListView.as_view()),
    path('postDetail/<int:pk>/', apis.PostDetail.as_view()),
    path('postLikeCreate/<int:post_pk>/', apis.PostLikeCreate.as_view()),
    path('commentCreate/<int:post_pk>/', apis.CommentView.as_view()),
    path('commentUpdateDelete/<int:pk>/', apis.CommentUpdateDelete.as_view()),
    path('postFiltering/', apis.PostFiltering.as_view()),
]
