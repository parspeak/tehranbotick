from django.contrib.auth.hashers import make_password


class UserPasswordUpdateMixin:
    def perform_update(self, serializer):
        password = serializer.validated_data.get('password')
        if password:
            serializer.validated_data['password'] = make_password(password)

        serializer.save()
