from .models import Mail
from rest_framework.serializers import ModelSerializer
from DjiStudio.utils import MyModelViewSet, AnyoneForbidden
from rest_framework import permissions


class MailSerializer(ModelSerializer):
    class Meta:
        model = Mail
        fields = ("__all__")


class IsAdminOrSelf(permissions.BasePermission):
    """
        Object-level permission to only allow modifications to a User object
        if you are modifying your own user object or administrator.
    """

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff or \
            request.user == obj.sender.user


class MailViewSet(MyModelViewSet):
    queryset = Mail.objects.all()
    serializer_class = MailSerializer

    permission_classes_by_action = {'destroy': [AnyoneForbidden],
                                    'list': [permissions.IsAdminUser],
                                    'retrieve': [IsAdminOrSelf]}

    def set_default_kv(self, request):
        return [
            {"sender": request.user.id}
        ]