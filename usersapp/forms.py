from datetime import datetime

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import django.forms as forms
from usersapp.models import RecipesUser

def add_form_control_class(fields):
    for _, field in fields.items():
        field.widget.attrs['class'] = "form-control"

class LoginForm(AuthenticationForm):

    class Meta:
        model = RecipesUser

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = "nickname"
        self.fields['password'].widget.attrs['placeholder'] = "password"
        add_form_control_class(self.fields)

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

        self.fields['nickname'].widget.attrs['placeholder'] = "nickname"
        self.fields['password1'].widget.attrs['placeholder'] = "password"
        self.fields['password2'].widget.attrs['placeholder'] = "password"
        
        add_form_control_class(self.fields)

    def clean_nickname(self):
        data = self.cleaned_data['nickname']
        if RecipesUser.objects.filter(nickname=data):
            raise forms.ValidationError(
                "Пользователь с таким никнеймом уже зарегистрирован")
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        if RecipesUser.objects.filter(email=data):
            raise forms.ValidationError(
                "Пользователь с таким email уже зарегистрирован")
        return data

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.user_id = self.retun_new_id()
        user.username = self.cleaned_data["nickname"]
        if commit:
            user.save()
        return user

    def retun_new_id(self):
        _pk = RecipesUser.objects.order_by('-pk')[0]
        _pk = str(_pk.pk+1)
        _year = str(datetime.now().year)
        _month = str(datetime.now().month)
        return (f'{_pk}-{_year}-{_month}')

class ChangeForm(forms.ModelForm):

    class Meta:
        model = RecipesUser
        fields = [
            'first_name', 
            'last_name',
            ]

    def __init__(self, *args, **kwargs):
        super(ChangeForm, self).__init__(*args, **kwargs)
        add_form_control_class(self.fields)