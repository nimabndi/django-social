from django import forms
from .models import Profile
from django.contrib.auth.models import User

messages = {
    'required': 'این فیلد اجباری است',
    'invalid': 'لطفا یک ایمیل معتبر وارد کنید',
    'max_length': 'تعداد کاراکترها بیشتر از حد مجاز است',
    'min_length': 'تعداد کاراکترها کمتر از حد مجاز است',
}


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(max_length=40,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class UserRegisterForm(forms.Form):
    username = forms.CharField(error_messages=messages, max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(error_messages=messages, max_length=50,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(error_messages=messages, max_length=40, min_length=8,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if username:
            user = User.objects.filter(username=username)
            if user.exists():
                raise forms.ValidationError('این نام کاربری از قبل وجود دارد')
            else:
                return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email:
            user_email = User.objects.filter(email=email)
            if user_email.exists():
                raise forms.ValidationError('این ایمیل از قبل وجود دارد')
            else:
                return email

    # def clean_password(self):
    #     password = self.cleaned_data['password']
    #     if password:
    #         if not password.isnumeric():
    #             raise forms.ValidationError('password number must be numeric')
    #         else:
    #             return password


class EditProfileForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = Profile
        fields = ('bio', 'age', 'phone')
        widgets = {'phone': forms.NumberInput(attrs={'disabled': ''})

                   }


class PhoneLoginForm(forms.Form):
    phone = forms.IntegerField()

    def clean_phone(self):
        phone = Profile.objects.filter(phone=self.cleaned_data['phone'])
        if not phone.exists():
            raise forms.ValidationError('This phone number does not exists')
        return self.cleaned_data['phone']


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class ChangePasswordForm(forms.Form):
    NewPassword = forms.CharField(error_messages=messages, max_length=40,
                                  widget=forms.PasswordInput(
                                      attrs={'class': 'form-control', 'placeholder': 'NewPassword'}))
