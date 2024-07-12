from django.urls import path
from . import views

urlpatterns = [
    # PATH CONVERTER
    # int: number
    # str: string
    # path: whole urls
    # slug: hyphen-and_underscore_stuff
    
    path('', views.home, name="home"),
    path('<int:year>/<str:month>', views.home, name="home"),
    path('all_events', views.all_events, name="all_events"),
    path('add_venue', views.add_venue, name="add_venue"),
    path('add_member', views.add_member, name="add_member"),
    path('list_venue', views.list_venue, name="list_venue"),
    path('show_venue/<venue_id>', views.show_venue, name="show_venue"),
    path('search_venue', views.search_venue, name="search_venue"),
    path('edit_venue/<venue_id>', views.edit_venue, name="edit_venue"),
    path('delete_venue/<venue_id>', views.delete_venue, name="delete_venue"),
    path('add_event', views.add_event, name="add_event"),
    path('edit_event/<event_id>', views.edit_event, name="edit_event"),
    path('delete_event/<event_id>', views.delete_event, name="delete_event"),
    path('list_members', views.list_members, name="list_members"),
    path('show_members/<myclubuser_id>', views.show_members, name="show_members"),
    path('venue_text', views.venue_text, name="venue_text"),
    path('venue_csv', views.venue_csv, name="venue_csv"),
    path('venue_pdf', views.venue_pdf, name="venue_pdf"),
    path('my_events', views.my_events, name="my_events"),
    path('search_events', views.search_events, name="search_events"),
    path('admin_approval', views.admin_approval, name="admin_approval"),
    path('venue_events/<venue_id>', views.venue_events, name="venue_events"),
     path('show_event/<event_id>', views.show_event, name="show_event"),
]
