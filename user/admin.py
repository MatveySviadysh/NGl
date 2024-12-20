from django.contrib import admin
from .models import Tutor, Review, UserProfile

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

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('username', 'rating', 'created_at')
    ordering = ('-created_at',)
    search_fields = ('username', 'comment')  

admin.site.register(Review, ReviewAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'avatar', 'description')
    search_fields = ('user__username', 'phone_number')