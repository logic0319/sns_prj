from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

UserModel = get_user_model()

__all__ = ('TokenSerializer', )


class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """
    user_email = serializers.SerializerMethodField()
    user_gender = serializers.SerializerMethodField()
    user_age = serializers.SerializerMethodField()
    user_latitude = serializers.SerializerMethodField()
    user_hardness = serializers.SerializerMethodField()
    user_registration_id = serializers.SerializerMethodField()

    class Meta:
        model = Token
        fields = ('key','user','user_email','user_gender','user_age','user_latitude','user_hardness',
                  'user_registration_id')

    def get_user_email(self,obj):
        return obj.user.email

    def get_user_gender(self,obj):
        return obj.user.gender

    def get_user_age(self,obj):
        return obj.user.age

    def get_user_latitude(self,obj):
        return obj.user.latitude

    def get_user_hardness(self,obj):
        return obj.user.hardness

    def get_user_registration_id(self, obj):
        return obj.user.registration_id
