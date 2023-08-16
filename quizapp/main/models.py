from django.db import models
from django.contrib.auth.models import User
from .models import models
# Create your models here.

# Otp

USER_TYPE_CHOICES = (
    ('admin', 'Admin'),
    ('teacher', 'Teacher'),
    ('student', 'Student'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    def __str__(self):
        return self.user
# new

class QuizCategory(models.Model):
    title = models.CharField(max_length=100)
    detail = models.TextField()
    image = models.ImageField(upload_to='cat_imgs/')
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.title
    
    
class QuizQuestion(models.Model):
    title = models.ForeignKey(QuizCategory, on_delete=models.CASCADE)
    question = models.TextField()
    opt_1 = models.CharField(max_length=200)
    opt_2 = models.CharField(max_length=200)
    opt_3 = models.CharField(max_length=200)
    opt_4 = models.CharField(max_length=200)
    level = models.CharField(max_length=100)
    time_limit= models.IntegerField()
    right_opt = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = 'Questions'
        
    def __str__(self):
        return self.question
    
    
class UserSubmittedAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    right_answer= models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = 'User Submitted Answers'

# New models
class Options(models.Model):
    opt = models.CharField(max_length=100)
    def __str__(self):
        return self.opt
    class Meta:
        verbose_name_plural = 'Options'
    
class OptionsQuestion(models.Model):
    title = models.ForeignKey(QuizCategory, on_delete=models.CASCADE)
    question = models.TextField(max_length=200)
    opt = models.ManyToManyField(Options)
    level = models.CharField(max_length=100)
    time_limit= models.IntegerField()
    right_opt= models.CharField(max_length=100)
        
    def __str__(self):
        return self.question
    class Meta:
        verbose_name_plural = 'Questions new'
        
# user submitt answer 
class UserSubmiteAnswer(models.Model):
    question = models.ForeignKey(OptionsQuestion, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    right_answer= models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = 'User Submitted Answers new'
    
#new userAttempt userCategoryAttempts
class UserCategoryAttempts(models.Model):
    category = models.ForeignKey(QuizCategory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attempt_time= models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'User Attempt Category'
        

    
    