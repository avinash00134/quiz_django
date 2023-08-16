from django.shortcuts import render,redirect
from django.forms import forms
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse,FileResponse
from .forms import AddQuestion,Category,NewAddQuestion,QuizCategory,RegistrationForm
from .models import Options,OptionsQuestion,UserCategoryAttempts
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
import datetime
from django.db.models import Sum 
# Create your views here.
def home(request):
    return render(request,'home.html')
def home_page(request):
    return render(request,'home_page.html')

    
# end def


from django.shortcuts import render
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user_type = form.cleaned_data.get('user_type')

            user = User.objects.create_user(username=username, password=password)

            if user_type == 'admin':
                user.is_staff = True
                user.is_superuser = True
            elif user_type == 'teacher':
                user.is_staff = True
            elif user_type == 'student':
                pass
            user.save()

            return render(request, 'registration/success.html')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})






# def register(request):
#     msg = None
#     form = RegisterUser()
#     if request.method=='POST':
#         form= RegisterUser(request.POST or None, request.FILES or None)
#         if form.is_valid():
#             user = form.save()
#             msg='Data has been added successfully..'
#             return redirect('login')
#         else:
#             form =RegisterUser()
#     return render(request,'registration/register.html',{'form':form,'msg':msg})
@staff_member_required
def attempt(request):
    data = models.UserCategoryAttempts.objects.all()
    return render(request,'registration/attempt.html',{'data':data})

def all_categories(request):
    catData = models.QuizCategory.objects.all()
    return render(request,'all-category.html',{'data':catData})

@staff_member_required
@login_required
def category_questions(request,cat_id):
    category  = models.QuizCategory.objects.get(id=cat_id)
    question = models.QuizQuestion.objects.filter(title=category).order_by('id').first()
    return render(request,'registration/category-questions.html',{'question':question, 'category':category})

# @login_required
# def submit_answer(request,cat_id,quest_id):
#     if request.method=='POST': 
#         category  = models.QuizCategory.objects.get(id=cat_id)
#         question = models.QuizQuestion.objects.filter(title=category,id__gt=quest_id).exclude(id=quest_id).order_by('id').first()
#         if 'skip' in request.POST:
#             if question:
#                 quest=models.QuizQuestion.objects.get(id=quest_id)
#                 user = request.user
#                 answer = 'Not Submitted'
#                 models.UserSubmittedAnswer.objects.create(user=user,question=quest,right_answer=answer)
#                 return render(request,'registration/category-questions.html',{'question':question, 'category':category})
#         else:
#             quest=models.QuizQuestion.objects.get(id=quest_id)
#             user = request.user
#             answer = request.POST['answer']
#             models.UserSubmittedAnswer.objects.create(user=user,question=quest,right_answer=answer)
#         if question:
#             return render(request,'registration/category-questions.html',{'question':question, 'category':category})
#         else:
#             return HttpResponse("There is no questions this section")
#     else:
#         return HttpResponse("It is no allowed Here..")
@login_required
@staff_member_required
def question(request):
    if request.method == "POST":
        form= AddQuestion(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            form= AddQuestion()
    else:
        form= AddQuestion()
    template= 'admin_add.html'
    context= {'title':'question','form':form}
    return render(request, template, context)

#new ADD UI
# @login_required
# def add_question(request):
#     if request.method == "POST":
#         form= NewAddQuestion(request.POST or None, request.FILES or None)
#         if form.is_valid():
#             form.save()
#             form= NewAddQuestion()
#     else:
#         form= NewAddQuestion()
#     template= 'new_add.html'
#     context= {'title':'question','form':form}
#     return render(request, template, context)

# Add all category
@login_required
@staff_member_required
def questioncat(request):
    if request.method == "POST":
        form= Category(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            form= Category()
    else:
        form= Category()
        
    template= 'admin_cat.html'
    context= {'title':'question','form':form}
    return render(request, template, context)



#news class defining
@login_required
@staff_member_required
def add_options(request):
    if request.method == "POST":
        form= Options(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            form= Options()
    else:
        form= Options()
    template= 'add_options.html'
    context= {'title1':'question','form':form}
    return render(request, template, context)
@login_required
@staff_member_required
def add_optionsquestion(request):
    if request.method == "POST":
        form= NewAddQuestion(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            form= NewAddQuestion()
    else:
        form= NewAddQuestion()
    template= 'add.html'
    context= {'title':'question','form':form}
    return render(request, template, context)

def all_category(request):
    cData = models.QuizCategory.objects.all()
    return render(request,'all-cat.html',{'data':cData})

#add the User only on attempt give the quiz
@login_required
def category_ques(request, cat_id):
    category = get_object_or_404(QuizCategory, id=cat_id)
    question = OptionsQuestion.objects.filter(title=category).order_by('id').first()

    # Get the most recent attempt for this user and category
    last_attempt =UserCategoryAttempts.objects.filter(user=request.user, category=category).order_by('-id').first()

    # If there is a previous attempt, check if the time limit has been reached
    if last_attempt is not None:
        future_time = last_attempt.attempt_time + timedelta(hours=24)
        if future_time > timezone.now():
            return redirect('attempt_limit')

    # Create a new attempt for this user and category
    UserCategoryAttempts.objects.create(user=request.user, category=category)

    return render(request, 'category-ques.html', {'question': question, 'category': category})

@login_required
def submitted_answer(request,cat_id,quest_id):
    if request.method=='POST': 
        title = models.QuizCategory.objects.get(id=cat_id)
        question = models.OptionsQuestion.objects.filter(title=title,id__gt=quest_id).exclude(id=quest_id).order_by('id').first()
        if 'skip' in request.POST:
            if question:
                quest=models.OptionsQuestion.objects.get(id=quest_id)
                user = request.user
                answer = 'Not Submitted'
                models.UserSubmiteAnswer.objects.create(user=user,question=quest,right_answer=answer)
                return render(request,'category-ques.html',{'question':question, 'category':title})
        else:
            quest=models.OptionsQuestion.objects.get(id=quest_id)
            user = request.user
            answer = request.POST['answer']
            models.UserSubmiteAnswer.objects.create(user=user,question=quest,right_answer=answer)
        if question:
            return render(request,'category-ques.html',{'question':question, 'category':title})
        else:
            result=models.UserSubmiteAnswer.objects.filter(user=request.user)
            skipQuestion=models.UserSubmiteAnswer.objects.filter(user=request.user,right_answer='Not Submitted').count()
            attempt=models.UserSubmiteAnswer.objects.filter(user=request.user).exclude(right_answer='Not Submitted').count()
            
            rightAnswer=0
            percentage=0
            for row in result:
                if row.question.right_opt == row.right_answer:
                    rightAnswer+=1    
            percentage=(rightAnswer*100)/result.count()
                
                
            return render(request,'registration/results.html',{'result':result,'total_skipped':skipQuestion,'attempt':attempt,'rightAnswer':rightAnswer,'percentage':percentage})
    else:
        return HttpResponse("It is no allowed Here..")
    
@login_required
def attempt_limit(request):
    return render(request,'registration/attempt-limit.html')
@login_required
def result(request):
    result=models.UserSubmiteAnswer.objects.filter(user=request.user)
    skipQuestion=models.UserSubmiteAnswer.objects.filter(user=request.user,right_answer='Not Submitted').count()
    attempt=models.UserSubmiteAnswer.objects.filter(user=request.user).exclude(right_answer='Not Submitted').count()
            
    rightAnswer=0
    percentage=0
    for row in result:
        if row.question.right_opt == row.right_answer:
            rightAnswer+=1    
    percentage=(rightAnswer*100)/result.count()                
    return render(request,'registration/results.html',{'result':result,'total_skipped':skipQuestion,'attempt':attempt,'rightAnswer':rightAnswer,'percentage':percentage})


# Download pdf result
# def download_pdf(request):
#     buf = io.BytesIO()
#     c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
#     textob = c.beginText()
#     textob.setTextOrigin(inch,inch)
#     textob.setFont("Helvetica",14)
#     lines = ["registration/results.html"]
#     for line in lines:
#         textob.textLine(line)
#     c.drawText(textob)
#     c.showPage()
#     c.save()
#     buf.seek(0)
#     return FileResponse(buf,as_attachment=True,filename='result.pdf')
@login_required
def download_pdf(request):
    response = HttpResponse(content_type ='application/pdf')
    response['Content-Disposition'] =' inline; attachment; filename=Expenses'+ str(datetime.datetime.now()) + '.pdf'
    response['Content-Transfer-Encoding']='binary'
    result=models.UserSubmiteAnswer.objects.filter(user=request.user)
    skipQuestion=models.UserSubmiteAnswer.objects.filter(user=request.user,right_answer='Not Submitted').count()
    attempt=models.UserSubmiteAnswer.objects.filter(user=request.user).exclude(right_answer='Not Submitted').count()
    rightAnswer=0
    percentage=0
    for row in result:
        if row.question.right_opt == row.right_answer:
            rightAnswer+=1    
    percentage=(rightAnswer*100)/result.count()
    sum=result.aaggregate(Sum('result','skipQuestion','attempt','rightAnswer','percentage'))   
    # html_string = render_to_string('my_template.html')
    html_string=render_to_string('registration/result.html',{'result':result,'total':sum ,'skipQuestion':skipQuestion,'attempt':attempt,'rightAnswer':rightAnswer,'percentage':percentage})
    html=HTML(string=html_string)
    result=html.write_pdf()
    
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        
        output=open(output.name, 'rb')
        response.write(output.read())
    return response



# Otp views
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
import math, random


def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(4) :
         OTP += digits[math.floor(random.random() * 10)]
     return OTP

def send_otp(request):
     email=request.GET.get("email")
     print(email)
     o=generateOTP()
     htmlgen = '<p>Your OTP is <strong>o</strong></p>'
     send_mail('OTP request',o,'<your gmail id>',[email], fail_silently=False, html_message=htmlgen)
     return HttpResponse(o)