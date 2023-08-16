from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# from .views import email_otp_verification, email_otp_verify

urlpatterns = [
    path('home/', views.home,name='home'),
    path('', views.home_page,name='home_page'),
    path('accounts/register', views.register,name='register'),
    # path('new-add/', views.add_question,name='add_question'),
    path('add/', views.question,name='question'),
    path('cat/', views.questioncat,name='questioncat'),
    #attempt limit url
    path('attemptlimit/', views.attempt_limit,name='attempt_limit'),
    path('result/', views.result,name='result'),
    
    path('addoption/', views.add_options,name='add_options'),
    path('addquestion/', views.add_optionsquestion,name='add_optionsquestion'),
    # Otp Verifications
    path("send_otp/",views.send_otp,name="send otp"),



    # path('email-otp-verification/', email_otp_verification, name='otp-verification'),
    # path('email-otp-verify/', email_otp_verify, name='otp-verify'),

    
    #downlod pdf 
    path('download/', views.download_pdf,name='download_pdf'),
    path('attempt/', views.attempt,name='attempt'),
    path('all-categories', views.all_categories,name='all_categories'),
    path('all-category', views.all_category,name='all_category'),
    # path('category-questions/', views.category_questions,name='category_questions'),
    path('category-ques/<int:cat_id>', views.category_ques,name='category_questions'),
    # path('submit-answer/<int:cat_id>/<int:quest_id>', views.submit_answer,name='submit_answer'),
    path('submitted-answer/<int:cat_id>/<int:quest_id>', views.submitted_answer,name='submitted_answer'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)