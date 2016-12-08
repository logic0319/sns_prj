from django.contrib.auth import logout as django_logout
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

__all__ = ('LogoutView', )


class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def get(self,request, *args, **kwargs):
        try:
            response = self.http_method_not_allowed(request, *args, **kwargs)
        except Exception as exc:
            response = self.handle_exception(exc)
        return self.finalize_response(request, response, *args, **kwargs)

    def post(self, request):
        return self.logout(request)

    def logout(self, request):
        request.user.auth_token.delete()
        django_logout(request)

        return Response({"success": "Successfully logged out."},
                        status=status.HTTP_200_OK)

