from django.contrib import admin
from main.models import Customer , Guide, Hike, EnrolledHikers, NewsLetter

# Register your models here.
admin.site.register(Customer)
admin.site.register(Guide)
admin.site.register(Hike)
admin.site.register(EnrolledHikers)
admin.site.register(NewsLetter)