from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm as _PasswordResetForm

class RhwNominateForm(forms.Form):
    idea = forms.ChoiceField()

    def xclean(self):
        raise Exception(self)


class PasswordResetForm(_PasswordResetForm):
    # ensure email ends with @redhat.com
    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@redhat.com'):
            raise forms.ValidationError('Only emails in domain redhat.com are allowed.')
        return email

    # create user if it does not exist
    def save(self, **kwargs):
        User = get_user_model()
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count() == 0:
            User.objects.create_user(
                username    = email[:-len('@redhat.com')],
                email       = email,
                password    = User.objects.make_random_password(),
            ).save()
        return super(PasswordResetForm, self).save(**kwargs)
