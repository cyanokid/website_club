from django.shortcuts import render, redirect
from django.contrib import messages
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from .models import Event, Venue, MyClubUser
from django.contrib.auth.models import User #untuk import model User dari django
from .forms import VenueForm, MyClubUserForm, EventForm, EventFormAdmin
import csv

#Import pdf stuff
from django.http import FileResponse
import io 
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

#Import pagination stuff
from django.core.paginator import Paginator



# Create your views here.
#Show Event 
def show_event(request, event_id):
    #pass specific object from event model
    event = Event.objects.get(pk=event_id)
    
    return render(request, 'events/show_event.html', {
        "event" : event,
    })
#Create list of Event page in Venue
def venue_events(request, venue_id):
    #Grab venue by ID
    venue = Venue.objects.get(id=venue_id)
    #Grab events from that venue
    events = venue.event_set.all()
    if events:
        return render(request, 'events/venue_events.html', {
            "events" : events,
        })

    else:
        messages.success(request, ("The Venue Has No Event At This Moment..."))   
        return redirect('admin_approval')

#Admin Event Approval page
def admin_approval(request):
    #Get Venues
    venue_list = Venue.objects.all()
    #Get counts
    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()

    #get the current time
    now = datetime.now()
    time = now.strftime('%A, %d/%m/%Y, %I:%M %p')

    event_list = Event.objects.all().order_by('-event_date')

    if request.user.is_superuser:
        if request.method == 'POST':

            #dapatkan id dari checkbox tadi, panggil guna nama dia 'boxes'
            id_list = request.POST.getlist('boxes')
            #Uncheck all events
            event_list.update(approved=False)
            #Update the database
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(approved=True)

            messages.success(request, ("Event Approval Has Been Updated!"))   
            return redirect('all_events')

        else:   
            return render(request, 'events/admin_approval.html', {
            "event_list" : event_list,
            "event_count" : event_count,
            "venue_count" : venue_count,
            "user_count" : user_count,
            "time" : time,
            "venue_list" : venue_list
        })
    else:
        messages.success(request, ("You Are Not Authorised To View This Page."))   
        return redirect('home')

    return render(request, 'events/admin_approval.html', {
    })

#search Events
def search_events(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        #jika yang dicari itu ada dalam name event. boleh juga cari yang contain in description
        events = Event.objects.filter(name__contains=searched)

        return render(request, 'events/search_events.html', {
            'searched': searched,
            'events': events,
        })
    else:
        return render(request, 'events/search_events.html', {
        })

#create My Events
def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events =  Event.objects.filter(manager=me) #guna attendies dok jadi, try letak manager dulu
        return render(request, 'events/my_events.html',{
            "events" : events, 
        })
    else:
        messages.success(request, ("You Are Not Authorised To View This Page."))   
        return redirect('home')




#create PDFfile
def venue_pdf(request):
    #Create Bystream buffer
    buf = io.BytesIO()
    #create a canvas/determine the page
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    #create a text object/ what to put
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    #Add some lines of text
    # lines = ["This is line 1",
    # "This is line 2",
    # "This is line 3"]

    # #Create a csv writer
    # writer = csv.writer(response)

    # #Designate the model
    venues = Venue.objects.all()

    # #add column heading to the csv file
    # writer.writerow(['Venue Name', 'Address', 'Zip Code', 'Phone', 'Web Address', 'Email Address'])

    #Create blank
    lines = []

    #Loop thu and output
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append("==================================================")
    
    #Loop
    for line in lines:
        textob.textLine(line)

    #Finish Up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    #Return
    return FileResponse(buf, as_attachment=True, filename='venue.pdf')

#create csvfile
def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'

    # lines = ["This is line 1 \n",
    # "This is line 2\n",
    # "This is line 3\n"]

    #Create a csv writer
    writer = csv.writer(response)

    #Designate the model
    venues = Venue.objects.all()

    #add column heading to the csv file
    writer.writerow(['Venue Name', 'Address', 'Zip Code', 'Phone', 'Web Address', 'Email Address'])

    #Loop thu and output
    for venue in venues:
       writer.writerow([ venue.name, venue.address, venue.zip_code, venue.phone, venue.web, venue.email_address])

    return response

#create textfile
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'

    # lines = ["This is line 1 \n",
    # "This is line 2\n",
    # "This is line 3\n"]

    #Designate the model
    venues = Venue.objects.all()

    #Create blank
    lines = []
    #Loop thu and output
    for venue in venues:
        lines.append(f'{venue.name}\n {venue.address}\n {venue.zip_code}\n {venue.phone}\n {venue.web}\n {venue.email_address}\n\n\n')

    #Write to TextFile
    response.writelines(lines)
    return response

def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, ("Event Deleted!!!"))
        return redirect('all_events')
    else:
        messages.success(request, ("You Are Not Authorized to Delete. Only Manager Can Delete This Event."))
        return redirect('all_events')


def show_members(request, myclubuser_id):
    #pass specific object from MyClubUser model
    myclubuser = MyClubUser.objects.get(pk=myclubuser_id)
    
    return render(request, 'events/show_members.html', {
        "myclubuser" : myclubuser,
    })

def list_members(request):
    #pass all of the object from MyClubUser model
    members_list = MyClubUser.objects.all()

    return render(request, 'events/list_members.html', {
        "members_list" : members_list,
    })
    
def edit_event(request, event_id):
    #pass specific object from venue model
    event = Event.objects.get(pk=event_id)
    #form for superuser
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)

    #form for user           
    #pass the posted form using instance
    else: 
        form = EventForm(request.POST or None, instance=event)

    if form.is_valid():
            form.save()
            return redirect('all_events')

    return render(request, 'events/edit_event.html', {
        "event" : event,
        "form" : form,
    })

def add_event(request):
    submitted = False
    if request.method == "POST":
        ##if we want to specify the user using id
        # if request.user.is_id == 4:

        #form for superuser
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        #form for other user
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user #loggedin user
                event.save()
                # form.save()
                return HttpResponseRedirect('/add_event?submitted=True')

    else:
        #Just going to the page, not submit it
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm

        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_event.html', {
            "form" : form,
            "submitted" : submitted,
        })

def delete_venue(request, venue_id):

    venue = Venue.objects.get(pk=venue_id)

    venue.delete()
    messages.success(request, ("Your venue has been deleted!"))   
    return redirect(request.META.get("HTTP_REFERER"))

def edit_venue(request, venue_id):
    #pass specific object from venue model
    venue = Venue.objects.get(pk=venue_id)
    #pass the posted form using instance
    form = VenueForm(request.POST or None, request.FILES or None, instance=venue)

    if form.is_valid():
            form.save()
            return redirect('list_venue')

    return render(request, 'events/edit_venue.html', {
        "venue" : venue,
        "form" : form,
    })

def search_venue(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)

        return render(request, 'events/search_venue.html', {
            'searched': searched,
            'venues': venues,
        })
    else:
        return render(request, 'events/search_venue.html', {
        })

def show_venue(request, venue_id):
    #pass specific object from venue model
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner) #connect venue owner dgn id manager
    
    #Cara nak ambil data dari foreign key, dalam kes ni nak ambil events dari venue tersebut
    events = venue.event_set.all()

    return render(request, 'events/show_venue.html', {
        "venue" : venue,
        "events" : events,
        "venue_owner" : venue_owner,
    })


def list_venue(request):
    #pass all of the object from Event model
    venue_list = Venue.objects.all()

    #Set up pagination
    p = Paginator(Venue.objects.all(), 10)
    page = request.GET.get('page')
    venues = p.get_page(page)
    #for pagination hack to show all pages
    nums = "a" * venues.paginator.num_pages

    return render(request, 'events/venue.html', {
        "venue_list" : venue_list,
        "venues" : venues,
        "nums" : nums,
    })

def add_member(request):
    submitted = False
    if request.method == "POST":
        form = MyClubUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_member?submitted=True')

    else:
        form = MyClubUserForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_member.html', {
            "form" : form,
            "submitted" : submitted,
        })

def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id #loggedin user
            venue.save()
            
            # form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')

    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_venue.html', {
            "form" : form,
            "submitted" : submitted,
        })

def all_events(request):

    #pass all of the object from Event model
    #ordering...
    event_list = Event.objects.all().order_by('-event_date')

    return render(request, 'events/event_list.html', {
        "event_list" : event_list,
    })

def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    month = month.title()

    name = "mawa"
    # convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # create calendar
    cal = HTMLCalendar().formatmonth(year, month_number)

    # get the current year
    now = datetime.now()
    current_year = now.year

    # query the Events Model for Dates
    event_list = Event.objects.filter(
        event_date__year = year,
        event_date__month = month_number,
    )

    # get current time
    time = now.strftime('%A %m/%Y %I:%M %p')

    #get the user
    me = request.user
 
    return render(request, 'events/home.html', {
        "name" : name,
        "year" : year,
        "month" : month,
        "month_number" : month_number,
        "cal" : cal,
        "now" : now,
        "current_year" : current_year,
        "time" : time,
        "event_list" : event_list,
        "me" : me,
    })
