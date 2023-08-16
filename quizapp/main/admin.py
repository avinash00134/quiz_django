from django.contrib import admin
from . import models
from .models import User



# Register your models here.
admin.site.register(models.QuizCategory)
admin.site.register(models.Options)

class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['question','level']    
admin.site.register(models.QuizQuestion,QuizQuestionAdmin)

class OptionsQuestionAdmin(admin.ModelAdmin):
    list_display = ['question','level']    
admin.site.register(models.OptionsQuestion,OptionsQuestionAdmin)

class UserSubmittedAnswerAdmin(admin.ModelAdmin):
    list_display = ['id','question','user','right_answer']    
admin.site.register(models.UserSubmittedAnswer,UserSubmittedAnswerAdmin)



class UserSubmiteAnswerAdmin(admin.ModelAdmin):
    list_display = ['id','question','user','right_answer']    
admin.site.register(models.UserSubmiteAnswer,UserSubmiteAnswerAdmin)

class UserCategoryAttemptsAdmin(admin.ModelAdmin):
    list_display = ['category','user','attempt_time']    
admin.site.register(models.UserCategoryAttempts,UserCategoryAttemptsAdmin)




