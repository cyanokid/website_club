from django import forms
from django.forms import ModelForm
from .models import Venue
from .models import MyClubUser
from .models import Event

#create a venue form
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ('name', 'address', 'zip_code', 'phone', 'web', 'email_address', 'venue_image')
        labels =  {
            'name' : '',
            'address' : '', 
            'zip_code' : '' , 
            'phone' : '', 
            'web' : '', 
            'email_address': '',
            'venue_image' : 'Upload Image :',
        }

        #to put css boostrap
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Venue Name'}),
            'address' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Venue Address'}), 
            'zip_code' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Zip Code'}), 
            'phone' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Phone Number'}), 
            'web' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Venue Website'}), 
            'email_address' : forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email Address'})
        }

#create a MyClubUser form        
class MyClubUserForm(ModelForm):
    class Meta:
        model = MyClubUser
        fields = ('first_name', 'last_name', 'email',)
        labels =  {
            'first_name' : '',
            'last_name' : '' , 
            'email' : '', 
        }

        #to put css boostrap
        widgets = {
            'first_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First Name'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last Name'}), 
            'email' : forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email'}), 
            }  

#create Admin SuperUser Event form        
class EventFormAdmin(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date', 'venue', 'manager', 'description', 'attendies')
        labels =  {
            'name' : '',
            'event_date' : 'Event Date' , 
            'venue' : 'Venue', 
            'manager' : 'Manager',
            'description' : '',
            'attendies' : 'Attendees',
        }

        #to put css boostrap
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Name'}),
            'event_date' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'YYYY-MM-DD'}), 
            'venue' : forms.Select(attrs={'class':'form-select', 'placeholder': 'Venue'}), 
            'manager' : forms.Select(attrs={'class':'form-select', 'placeholder': 'Manager'}), 
            'description' : forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Description'}), 
            'attendies' : forms.SelectMultiple(attrs={'class':'form-select', 'placeholder': 'Attendee'}), 
           }  

#create User Event form        
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date', 'venue', 'description', 'attendies')
        labels =  {
            'name' : '',
            'event_date' : 'Event Date' , 
            'venue' : 'Venue', 
            'description' : '',
            'attendies' : 'Attendees',
        }

        #to put css boostrap
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Name'}),
            'event_date' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'YYYY-MM-DD'}), 
            'venue' : forms.Select(attrs={'class':'form-select', 'placeholder': 'Venue'}), 
            'description' : forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Description'}), 
            'attendies' : forms.SelectMultiple(attrs={'class':'form-select', 'placeholder': 'Attendee'}), 
           }  




