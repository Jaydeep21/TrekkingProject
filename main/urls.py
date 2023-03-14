from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('treks', views.treks, name='treks'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.logout_view,  name='logout'),
    path('booking/<int:id>', views.booking,  name='booking'),
    path('signup', views.Signup.as_view(), name='signup'),
    path('singleTrek/<int:id>', views.singleTrek, name='trek'),
]