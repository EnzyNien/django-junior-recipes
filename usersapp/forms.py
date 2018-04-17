from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
import django.forms as forms
from usersapp.models import RecipesUser

class LoginForm(AuthenticationForm):

    class Meta:
        model = RecipesUser

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = "nickname or ID"
        self.fields['password'].widget.attrs['placeholder'] = "password"
        self.fields['username'].widget.attrs['class'] = "form-control"
        self.fields['password'].widget.attrs['class'] = "form-control"

    def clean(self):
        nickname_or_id = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if nickname_or_id and password:
            username_from_nickname = RecipesUser.objects.filter(nickname=nickname_or_id)
            username_from_ID = RecipesUser.objects.filter(user_id=nickname_or_id)
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

class RegistrationForm(UserCreationForm):

    class Meta:
        model = RecipesUser
        fields = [
            'email',
            'nickname',
            'password1',
            'password2'
            ]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['nickname'].widget.attrs['placeholder'] = "nickname or ID"
        self.fields['password1'].widget.attrs['placeholder'] = "password"
        self.fields['password2'].widget.attrs['placeholder'] = "password"

        for _, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"

    def clean_nickname(self):
        data = self.cleaned_data['nickname']
        if RecipesUser.objects.filter(nickname=data):
            raise forms.ValidationError(
                "Пользователь с таким же никнеймом уже зарегистрирован")
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        if RecipesUser.objects.filter(email=data):
            raise forms.ValidationError(
                "Пользователь с таким же email уже зарегистрирован")
        return data
