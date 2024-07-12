from django.db import models
from django.contrib.auth.models import User #django built in user
from datetime import date

# Create your models here.
class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip Code', max_length=15)
    phone = models.CharField('Contact Phone', max_length=25, blank=True)
    web = models.URLField('Website Address', blank=True )
    email_address = models.EmailField('Email Address', blank=True)
    #default here means it will start with number=1
    owner = models.IntegerField('Venue Owner',  blank=True, default= 1)
    venue_image = models.ImageField(null=True, blank=True, upload_to="images/")
    
    def __str__(self):
        return self.name

class MyClubUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email =  models.EmailField('User Email')

    def __str__(self):
        return self.first_name +  ' ' + self.last_name

class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')

    #we want to connect venue in event model to venue model
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    #SET_NULL means not to delete all but just put null
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    #its ok to not fill the textfield
    description = models.TextField(blank=True)

    #many-to-many = users and events
    attendies = models.ManyToManyField(MyClubUser, blank=True)
    #only true or false to approval
    #by default it is false
    approved = models.BooleanField('Approved', default=False)

    def __str__(self):
        return self.name

    @property
    def Days_till(self):
        today = date.today()
        days_till = self.event_date.date() - today
        #just want to return the first splite, that is the day. second split which are times are not included
        days_till_stripped = str(days_till).split(",", 1)[0]
        return days_till_stripped

    @property
    def Is_Past(self):

        today = date.today()

        if self.event_date.date() < today:
            thing = "Past"

        elif self.event_date.date() == today:
            thing = "Ongoing"

        else:
            thing = "Future"
        
        return thing