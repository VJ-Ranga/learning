import secrets
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm


class JoinForm(UserCreationForm):
    invite_code = forms.CharField(label='Learning room invite code', widget=forms.PasswordInput)

    def clean_invite_code(self):
        value = self.cleaned_data['invite_code']
        if not settings.ENROLLMENT_CODE or not secrets.compare_digest(value.encode('utf-8'), settings.ENROLLMENT_CODE.encode('utf-8')):
            raise forms.ValidationError('That invite code is not valid. Ask your learning partner for the room code.')
        return value
