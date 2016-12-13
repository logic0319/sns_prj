from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


from member.models import CustomUser as User
from member.serializers.userprofile import UserProfileSerializer

__all__ = ('UserProfileView', )


class UserProfileView(GenericAPIView):
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = User.objects.get(pk=request.user.pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)








