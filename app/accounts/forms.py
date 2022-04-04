from accounts.models import User

from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


class SignUpForm(forms.ModelForm):
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    confirm = forms.CharField(required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password', 'confirm')

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data['password'] != cleaned_data['confirm']:
            raise forms.ValidationError('Passwords should match!')

        return cleaned_data

    def save(self, commit=True):
        cleaned_data = self.cleaned_data

        user = super().save(commit=False)
        user.set_password(cleaned_data['password'])
        user.is_active = False

        if commit:
            user.save()

        self._send_activation_email(user)

        return user

    @staticmethod
    def _send_activation_email(user):
        subject = f'''Registration at {settings.DOMAIN}'''
        message_body = f'''
        You registered an account on {settings.DOMAIN}, before being able to use your 
        account you need to verify that this is your email address by clicking here:
        {settings.HTTP_SCHEMA}://{settings.DOMAIN}{reverse('accounts:activate-user',args=[user.username])} 

        Kind Regards, {settings.DOMAIN}
        '''
        email_from = settings.EMAIL_HOST_USER
        send_mail(
            subject,
            message_body,
            email_from,
            [user.email],
            fail_silently=False,
        )
