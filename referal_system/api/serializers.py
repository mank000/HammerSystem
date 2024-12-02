from rest_framework import serializers

from phone_numbers.models import HammerSystemUser
from phone_numbers.utils import (generate_invite_code,
                                 generate_verifircation_code)


class RegistrationSerializer(serializers.ModelSerializer):
    auth_code = serializers.CharField(read_only=True)

    class Meta:
        model = HammerSystemUser
        fields = ('phone', 'auth_code')

    def create(self, validated_data):
        user = HammerSystemUser.objects.create(
            phone=validated_data['phone'],
            auth_code=generate_verifircation_code(),
            invite_code=generate_invite_code()
        )

        # send_auth_code(user.phone, user.auth_code)
        user.save()
        return user


class NewCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate(self, validated_data):
        try:
            user = HammerSystemUser.objects.get(phone=validated_data['phone'])
            user.auth_code = generate_verifircation_code()
            user.save()
            # send_auth_code()
            return user
        except HammerSystemUser.DoesNotExist:
            raise serializers.ValidationError(
                "Пользователь с таким номером не найден.")


class VerificationSerializer(serializers.Serializer):
    phone = serializers.CharField()
    verification_code = serializers.CharField()

    def validate(self, data):
        try:
            user = HammerSystemUser.objects.get(phone=data['phone'])
            if user.auth_code == data['verification_code']:
                user.is_verified = True
                user.auth_code = None
                user.save()
                return user
            raise serializers.ValidationError("Неверный код подтверждения.")
        except HammerSystemUser.DoesNotExist:
            raise serializers.ValidationError(
                "Пользователь с таким номером не найден.")


class ProfileSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(read_only=True)  # Поле для номера телефона
    users_invited = serializers.SerializerMethodField()
    invite_code = serializers.CharField()

    class Meta:
        model = HammerSystemUser
        fields = ('id', 'phone', 'invite_code', 'users_invited')

    def get_users_invited(self, obj):
        invited_users = HammerSystemUser.objects.filter(
            invite_code=obj.invite_code).exclude(id=obj.id)
        return [str(user.phone) for user in invited_users]

    def validate_invite_code(self, invite_code):
        user = self.instance
        if invite_code == user.invite_code:
            raise serializers.ValidationError(
                'Нельзя ввести свой собственный инвайт код.')
        if user.invite_code_changed:
            raise serializers.ValidationError(
                'Вы уже активировали инвайт код.')
        if not HammerSystemUser.objects.filter(
                invite_code=invite_code).exists():
            raise serializers.ValidationError(
                'Такого инвайт кода не существует.')

        return invite_code

    def update(self, instance, validated_data):
        invite_code = validated_data.get('invite_code', instance.invite_code)
        instance.invite_code = invite_code
        instance.invite_code_changed = True
        instance.save()
        return instance
