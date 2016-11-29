from rest_framework import serializers

from member.models import CustomUser


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    gender = serializers.BooleanField(required=False)
    age = serializers.DateField(required=False)

    def create(self, validated_data):
        validated_data = {
            'email': validated_data.get('email', ''),
            'password': validated_data.get('password1', ''),
            'gender': validated_data.get('gender'),
            'age': validated_data.get('age'),
        }
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data

