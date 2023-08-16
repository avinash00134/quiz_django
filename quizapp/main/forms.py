from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import QuizQuestion,QuizCategory,OptionsQuestion,Options,USER_TYPE_CHOICES,UserCategoryAttempts
from django import forms


# class RegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     re_password = forms.CharField(widget=forms.PasswordInput)
#     user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)
#     class Meta:
#         model = User
#         fields = ('first_name','last_name','username','email','password','re_password','user_type')
        
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError('Email already exists.')
#         return email
#     def clean_re_password(self):
#         password1 = self.cleaned_data['password']
#         password2 = self.cleaned_data['re_password']
#         if password1 != password2:
#             raise forms.ValidationError('Passwords do not match.')
#         return password2
    
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.email = self.cleaned_data['email']
#         user.user_type = self.cleaned_data['user_type']
#         user.set_password(self.cleaned_data['password'])
#         if commit:
#             user.save()
#         return user
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

# Otp




class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    re_password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 're_password', 'user_type')
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists.')
        return email
    
    def clean_re_password(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['re_password']
        if password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.user_type = self.cleaned_data['user_type']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


            # Create a UserProfile object and save it


        
class AddQuestion(forms.ModelForm):
    question=forms.Textarea()
    opt_1 =forms.CharField()
    opt_2 =forms.CharField()
    opt_3 =forms.CharField()
    opt_4 =forms.CharField()
    level = forms.CharField()
    time_limit= forms.IntegerField()
    right_opt = forms.CharField()
    class Meta:
        model= QuizQuestion
        fields= ('title','question','opt_1','opt_2','opt_3','opt_4','level','time_limit','right_opt')
        
#add new class model UI and add the condition option field take the      
class NewAddQuestion(forms.ModelForm):
    question = forms.CharField(widget=forms.Textarea)
    opt =forms.CharField(widget=forms.TextInput)
    level = forms.CharField()
    time_limit = forms.IntegerField()
    right_opt = forms.CharField()

    class Meta:
        model = OptionsQuestion
        fields = ('title', 'question', 'opt', 'level', 'time_limit', 'right_opt')

    def clean_opt(self):
        options = self.cleaned_data['opt'].split(',')
        cleaned_options = []
        for option in options:
            option = option.strip()
            if option:
                cleaned_options.append(option)
        return cleaned_options

    def save(self, commit=True):
        question = super().save(commit=False)
        if commit:
            question.save()
        for option in self.cleaned_data['opt']:
            opt, _ = Options.objects.get_or_create(opt=option)
            question.opt.add(opt)
        return question       
        
class Category(forms.ModelForm):
    title = forms.CharField()
    detail = forms.CharField()
    image = forms.ImageField()
    
    class Meta:
        model= QuizCategory
        fields= ('title','detail','image')
        
class Attempt(forms.ModelForm):
    category = forms.CharField()
    user = forms.CharField()    
    class Meta:
        model= UserCategoryAttempts
        fields= ('category','user')