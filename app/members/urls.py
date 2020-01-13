from django.urls import path

from members import apis

urlpatterns_api_members = [
    path('authToken/', apis.AuthTokenView.as_view()),
    path('signup/', apis.SignupView.as_view()),
    path('profile/', apis.UserProfileView.as_view()),
    path('logout/', apis.LogoutView.as_view()),
    path('checkID/', apis.CheckUniqueIDView.as_view()),
    path('followerUser/', apis.FollowerView.as_view()),
    path('followingUser/', apis.FollowingView.as_view()),
    # path('check-password/', apis.CheckPasswordView.as_view()),
]
