from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    객체의 소유자만, 쓰기를 허용하는 커스텀 권한
    """

    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모두에게 허용
        # Get, Head, Options 요청은 항상 허용한다.
        if request.method in permissions.SAFE_METHODS:
            return True

        # 쓰기 권한은 코드 조각의 소유자에게만 부여한다.
            return obj.auth_token == request.user.auth_token
