from django.contrib import admin

from .models import Venue
from .models import Event
from .models import MyClubUser

from django.contrib.auth.models import Group

# Register your models here.
#admin.site.register(Venue)
# admin.site.register(Event)
admin.site.register(MyClubUser)

# Unregister
# Remove Groups 
# admin.site.unregister(Group)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    #what we can do with admin model
    list_display = ('name', 'address', 'phone') #to add column
    ordering = ('name',) #ordering
    search_fields = ('name', 'address') #add searchbar

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    #what we can do with admin model
    fields = (('name', 'venue'), 'manager', 'event_date', 'description', 'approved') #to add column
    list_display = ('name', 'event_date', 'venue')
    list_filter = ('event_date', 'venue')
    ordering = ('-event_date',) #ordering