from django.contrib import admin
from . models import User,Profile, Room, Topic, Message

class UserAdmin(admin.ModelAdmin):
    list_display=['full_name','email']

class ProfileAdmin(admin.ModelAdmin):
    list_display=['full_name','gender','country']
    # list_editable = ['gender','country']
    search_fields = ['full_name','gender','country']
    list_filter = ['date']

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)


admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
