from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('treks', views.treks, name='treks'),
    path('forget-password' , views.ForgetPassword , name="forget_password"),
    path('change-password/<token>/' , views.ChangePassword , name="change_password"),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.logout_view,  name='logout'),
    path('booking/<int:id>', views.booking,  name='booking'),
    path('signup', views.Signup.as_view(), name='signup'),
    path('singleTrek/<int:id>', views.singleTrek, name='trek'),
    path('bookings', views.myBooking, name='bookings'),
    path('team', views.teams, name='team'),
    path('payment/<int:id>', views.payment, name='payment'),
    path('profile', views.profile, name='profile'),
    path('contact', views.contact, name='contact'),
    path('cancel/<int:id>', views.cancelBooking, name='cancel'),
    # path('email', views.email, name='email'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)