from django import forms

from .models import HammerSystemUser


class RegistrationForm(forms.Form):
    phone = forms.CharField(max_length=15)

    def clean_phone(self):
        phone_number = self.cleaned_data['phone']
        return phone_number


class VerificationForm(forms.ModelForm):
    class Meta:
        model = HammerSystemUser
        fields = ['auth_code']
    auth_code = forms.CharField(label="Код подтверждения")


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = HammerSystemUser
        fields = ['invite_code']
    invite_code = forms.CharField(label="Инвайт код")

    def clean_invite_code(self):
        invite_code = self.cleaned_data.get('invite_code')
        user = self.instance

        if invite_code == user.invite_code:
            raise forms.ValidationError(
                'Нельзя ввести свой собственный инвайт код.')

        if user.invite_code_changed:
            raise forms.ValidationError('Вы уже активировали инвайт код.')

        if not HammerSystemUser.objects.filter(
                invite_code=invite_code).exists():
            raise forms.ValidationError('Такого инвайт кода не существует.')

        return invite_code
