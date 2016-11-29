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
        print(validated_data)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data

    # def get_cleaned_data(self):
    #     return {
    #         'email': self.validated_data.get('email', ''),
    #         'password1': self.validated_data.get('password1', ''),
    #         'gender': self.validated_data.get('gender', ''),
    #         'age': self.validated_data.get('age', ''),
    #     }

    # def save(self, request):
    #     super(self, RegisterSerializer).save()
    #     user = adapter.new_user(request)
    #     self.cleaned_data = self.get_cleaned_data()
    #     adapter.save_user(request, user, self)
    #     setup_user_email(request, user, [])
    #     return user


