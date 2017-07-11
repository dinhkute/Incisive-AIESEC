from django import forms
from django.contrib.auth.models import User
#from django.contrib.auth import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import (UserProfile,
                     RecruitmentForm,
                     Questionnaire,
                     RegisterEvent,)

class RegisterForm(UserCreationForm):
    email= forms.EmailField(required=True)

    class Meta:
        model = User
        fields = {'username',
                  'first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2'}

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = {
            'first_name',
            'last_name',
            'email',
            'password'
            }

class RecruitmentDataForm(forms.ModelForm):
    student_name = forms.CharField()

    class Meta:
        model = RecruitmentForm
        fields = {'student_name',}

class Answer(forms.ModelForm):
    answer = forms.CharField()

    class Meta:
        model = Questionnaire
        fields = {'answer',}

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = {'answer', 'question_name'}

    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['question_name'].widget.attrs['readonly'] = True


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()

class EventRegister(forms.ModelForm):
    class Meta:
        model = RegisterEvent
        fields = {'customer_name','customer_phone','customer_email',}