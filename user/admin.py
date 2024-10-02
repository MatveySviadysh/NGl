from django.contrib import admin
from .models import Tutor

class TutorAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 
        'email', 
        'phone_number', 
        'specialization', 
        'avatar', 
        'tutor_id', 
        'rating', 
        'experience', 
        'video', 
        'verified', 
        'services', 
        'price'
    )
    search_fields = ('email', 'full_name', 'phone_number')

admin.site.register(Tutor, TutorAdmin)
