from rest_framework.response import Response
# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView

from .models import Users
from .serializers import UserProfileSerializer, ChangePasswordSerializer
from .permissions import IsOwnerOrReadOnly


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list와 detail 기능 자동 지원
    """
    queryset = Users.objects.all()
    serializer_class = UserProfileSerializer


class UserModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet 은 'list', 'create', 'retrieve', 'update', 'destroy' 기능을 지원한다.
    """
    queryset = Users.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )


class UpdatePassword(APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
