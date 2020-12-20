from django.contrib import admin
from .models import User,SiteAnnouncement,Contact,Profile
# Register your models here.
class ContactRef(admin.ModelAdmin):
    list_display = ['name','email','phone','message']

class SiteAnnouncementRef(admin.ModelAdmin):
    list_display = ['message','link']

admin.site.register(User)
admin.site.register(Contact,ContactRef)
admin.site.register(SiteAnnouncement,SiteAnnouncementRef)
admin.site.register(Profile)