from django.urls import path, include
from rest_framework.routers import DefaultRouter

from members import apis
from members import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'usersModelView', views.UserModelViewSet)

urlpatterns_api_members = [
    path('authToken/', apis.AuthTokenView.as_view()),
    path('signup/', apis.SignupView.as_view()),
    path('logout/', apis.LogoutView.as_view()),
    path('checkID/', apis.CheckUniqueIDView.as_view()),
    path('followerUser/', apis.FollowerView.as_view()),
    path('followingUser/', apis.FollowingView.as_view()),
    path('', include(router.urls)),
    path('changePassword/', views.UpdatePassword.as_view()),
    path('myProfile/', apis.MyProfileView.as_view()),
    path('myPostLikeList/', apis.PostLIkeListView.as_view()),
    path('relationship/', apis.FollowUserView.as_view()),
    path('facebook-login/', views.facebook_login, name='facebook-login'),
]
