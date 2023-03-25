from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import  UserLoginForm
from .models import Customer, Hike, Guide, EnrolledHikers, NewsLetter
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.views.decorators.debug import sensitive_variables
from django.conf import settings
from django.db.models import F
from django.contrib import messages

# Create your views here.
def base(request):
    return render(request, 'base.html')

def index(request):
    list(messages.get_messages(request))
    if request.method == 'POST':
        if NewsLetter.objects.filter(email = request.POST.get("email")):
            messages.error(request, 'You are already registered with us!')
            return HttpResponseRedirect(reverse('main:index'))
        else:
            newsLetter = NewsLetter()
            newsLetter.name =  request.POST.get("name")
            newsLetter.email =  request.POST.get("email")
            newsLetter.save()
            messages.success(request, 'You are successfully registered with us!')
            return HttpResponseRedirect(reverse("main:index"))        
    return render(request, 'index.html', {"treks": Hike.objects.all()})

def singleTrek(request, id):
    trek = get_object_or_404(Hike , pk = id)
    user = get_object_or_404(Guide, pk=trek.user_id )
    print("User id", user)
    if trek is None or user is None:
        return redirect('/treks')
    return render(request, 'treks-single.html', {"trek": trek, "user": user})

@login_required(login_url='main:login')
def treks(request):
    enrolledHikers = EnrolledHikers.objects.filter(user=request.user.pk).values_list('hike')
    if request.method == "GET":
        search_text = request.GET.get('search')
        # print(search_text)
        if search_text is not None:
            occupied_treks = Hike.objects.filter(available_capcity__gte=F('group_size')).exclude(pk__in=enrolledHikers).filter(mountain__contains=search_text)

            available_treks = Hike.objects.filter(group_size__gt=F('available_capcity')).exclude(pk__in=enrolledHikers).filter(mountain__contains=search_text)

        else:
            # enrolledHikers brings list of treks which user has enrolled into

            # occupied_treks searches for all the treks which are already full and removes treks which user has already enrolled to
            occupied_treks = Hike.objects.filter(available_capcity__gte = F('group_size')).exclude(pk__in=enrolledHikers)

            # available_treks first filters which treks are available and excludes all the treks which user is already a part of
            available_treks = Hike.objects.filter(group_size__gt = F('available_capcity')).exclude(pk__in=enrolledHikers)
    # print(available_treks)
    return render(request, 'treks.html', {"treks": available_treks, "occupied_treks": occupied_treks})

@login_required(login_url='main:login')
def myBooking(request):

    # enrolledHikers brings list of treks which user has enrolled into
    enrolledHikers = EnrolledHikers.objects.filter(user = request.user.pk).values_list('hike')
    if request.method == "GET":
        search_text = request.GET.get('search')
        # print(search_text)
        if search_text is not None:
            booked_treks = Hike.objects.filter(pk__in=enrolledHikers).filter(mountain__contains=search_text)
        else:
    # booked_treks searches all the treks which logged in user is enrolled to
            booked_treks = Hike.objects.filter(pk__in = enrolledHikers)

    return render(request, 'booking.html' ,{"booked_treks": booked_treks})

@login_required(login_url='main:login')
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url='main:login')
def booking(request, id):
    try:
        hikeCheck = EnrolledHikers.objects.get(user=request.user.pk, hike = id)
    except EnrolledHikers.DoesNotExist:
        hikeCheck = None
    if hikeCheck is not None:
       return redirect(request.META.get('HTTP_REFERER', '/'), {"error", "Sorry you've already enrolled for this trek"})
    hike = Hike.objects.get(pk=id)
    if hike is None:
        return redirect(request.META.get('HTTP_REFERER', '/'), {"error":"Sorry, no such trek exists"})
    if hike.available_capcity >= hike.group_size:
        return redirect(request.META.get('HTTP_REFERER', '/'), {"error":"Sorry, you're late group capacity is full"})        
    enrolledHikers = EnrolledHikers.objects.create(hike = hike, user = Customer.objects.get(pk = request.user.pk))
    hike.available_capcity += 1
    hike.save()
    if hasattr(settings, 'EMAIL_HOST_USER') and hasattr(settings, 'EMAIL_HOST_PASSWORD'):            
        email(request, enrolledHikers.pk)
    return redirect('/bookings')

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
        user.first_name = request.POST.get("fname")
        user.last_name = request.POST.get("lname")
        user.password = make_password(request.POST.get("password"))
        user.save()
        return redirect('/', {"success": "User details stored successfully"})

@login_required(login_url='main:login')
def email(request, id):
    hike = EnrolledHikers.objects.get(pk=id)
    tx = float("{:.2f}".format(hike.hike.cost * .13))
    total = tx + hike.hike.cost
    htmly = get_template('email.html')
    subject, from_email, to = 'Booking Confirmation', 'from@example.com', request.user.email
    html_content = htmly.render({"hike": hike, "tax": tx, "total":total })
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.content_subtype = "html"
    msg.send()
    print(msg)
    # return render(request, 'email.html', {"hike": hike, "tax": tx, "total":total } )

def teams(request):
    return render(request, "team.html", {"team": Guide.objects.all()})