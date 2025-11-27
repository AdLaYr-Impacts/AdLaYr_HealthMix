from django import forms
from .models import Profile

class RegisterForm(forms.ModelForm):

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'confirm_password',
            'class': 'form-control form-input',
            'required': 'required',
            'placeholder': 'Confirm password'
        }),
        label="Confirm Password"
    )

    class Meta:
        model = Profile
        fields = ['username', 'email', 'password']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control form-input',
                'required': 'required', 
                'placeholder': 'Enter your name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-input',
                'required': 'required',
                'placeholder': "example@gmail.com"
            }),
            'password': forms.PasswordInput(attrs={
                'id': 'password',
                'class': 'form-control form-input',
                'required': 'required',
                'placeholder': 'Enter password'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords didn't match")
        return cleaned_data
    
    def save(self, commit = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    

class LoginForm(forms.Form):

    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control input-glow',
        'placeholder': "User Name",
        'required': 'required'
    }))

    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'id': 'password',
        'class': 'form-control input-glow',
        'placeholder': "password",
        'required': 'required'
    }))