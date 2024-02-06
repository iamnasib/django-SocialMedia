from dataclasses import field
from datetime import datetime
from pyexpat import model
from statistics import mode
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,AuthenticationForm
from .models import MyUser, Posts, Comments, Tales
from .validators import validate_email

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Firstname',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Lastname',
                                                               'class': 'form-control',
                                                               }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(validators = [validate_email],required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta(UserCreationForm):
        model = MyUser
        fields = ('full_name','username', 'email', 'password1', 'password2')


class MyUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = MyUser
        fields = ('username', 'mobile_number', 'full_name', 'DOB',
                  'is_private', 'bio', 'website', 'DP', 'followers','blocked_user')

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = MyUser
        fields = ['username', 'password', 'remember_me']

class UpdateUserForm(forms.ModelForm):
    DP=forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file d-none',
                                               'id':'dp','onchange' : "myFunction();"}))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder':'Username'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                    'placeholder':'Email'}))
    full_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Name',
                                                               'class': 'form-control',
                                                               }))
    mobile_number=forms.CharField(max_length=10,
                                  required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder':'Mobile Number'}))
    bio=forms.CharField(max_length=250,
                        required=False,
                        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                                'placeholder':'Bio'}))
    DOB=forms.DateField(required=False,
                        widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'}))
    website=forms.URLField(required=False,
                           widget=forms.URLInput(attrs={'class': 'form-control',
                                                'placeholder':'Website'}))
    is_private=forms.CheckboxInput(attrs={'class': 'form-check-input'})


    class Meta:
        model = MyUser
        fields = ['DP','username', 'email', 'full_name','mobile_number','bio','DOB','website','is_private']

class UploadPostForm(forms.ModelForm):
    post_image=forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file d-none',
                                                      'id':'dp','onchange' : "readURL(this);"}))
    caption = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                    'placeholder':'Caption', 'required':'false',
                                                    'rows': 3}))
    comments_disabled=forms.CheckboxInput(attrs={'class': 'form-check-input'})


    class Meta:
        model=Posts
        fields=['post_image','caption','comments_disabled']

class EditPostForm(forms.ModelForm):
    post_image=forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file ',
                                                      'id':'dp'}))
    captionn = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                    'placeholder':'Comment','id':'comment'
                                                    }))
    class Meta:
        model=Posts
        fields=['post_image','captionn']

class NewCommentForm(forms.ModelForm):
    comment=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                    'placeholder':'Comment','id':'comment'
                                                    }))
    class Meta:
        model=Comments
        fields=['comment']

class TalesForm(forms.ModelForm):
    file=forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control-file d-none ',
                                                'onchange' : "readURLTales(this);",'id':'file',
                                                      }))
    class Meta:
        model=Tales
        fields=['file']
