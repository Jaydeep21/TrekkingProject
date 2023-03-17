from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms import  UserLoginForm
from .models import Customer, Hike, Guide, EnrolledHikers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.views.decorators.debug import sensitive_variables
from django.conf import settings


# Create your views here.
def base(request):
    return render(request, 'base.html')

def index(request):
    return render(request, 'index.html')

def singleTrek(request, id):
    trek = get_object_or_404(Hike , pk = id)
    user = get_object_or_404(Guide, pk=trek.user_id  )
    print("User id", user)
    if trek is None or user is None:
        return redirect('/treks')
    return render(request, 'treks-single.html', {"trek": trek, "user": user})

def treks(request):
    return render(request, 'treks.html', {"treks": Hike.objects.all()})

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url='login')
def booking(request, id):
    hike = Hike.objects.get(pk=id)
    print("User", request.user.pk)
    if hike is None:
        return redirect(request.META.get('HTTP_REFERER', '/'), {"error":"Sorry, no such trek exists"})
    enrolledHikers = EnrolledHikers.objects.create(hike = hike, user = Customer.objects.get(pk = request.user.pk))
    if hasattr(settings, 'EMAIL_HOST_USER') and hasattr(settings, 'EMAIL_HOST_PASSWORD'):            
        email(request, enrolledHikers.pk)
    return redirect('/')

class Login(View):
    form = UserLoginForm
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'login.html', {"form": self.form})
        else:
            return redirect('/')
    
    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login.html', {"form": self.form, "error" : 'Invalid username or password.'})

class Signup(View):
    # form = SignupForm
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'registration.html')
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    
    def post(self, request, *args, **kwargs):
        user = Customer()
        user.username = request.POST.get("email")
        user.email = request.POST.get("email")
        user.phone = request.POST.get("phone")
        user.age = request.POST.get("age")
        user.fname = request.POST.get("fname")
        user.lname = request.POST.get("lname")
        user.password = make_password(request.POST.get("password"))
        user.save()
        return redirect('/', {"success": "User details stored successfully"})

@login_required
def email(request, id):
    hike = EnrolledHikers.objects.get(pk=id)
    tx = float("{:.2f}".format(hike.hike.cost * .13))
    total = tx + hike.hike.cost
    htmly = get_template('email.html')
    subject, from_email, to = 'Booking Confirnmation', 'from@example.com', request.user.email
    html_content = htmly.render({"hike": hike, "tax": tx, "total":total })
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.content_subtype = "html"
    msg.send()
    print(msg)
    # return render(request, 'email.html', {"hike": hike, "tax": tx, "total":total } )