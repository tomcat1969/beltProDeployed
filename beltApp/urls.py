from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('regist',views.regist),
    path('dashboard',views.dashboard),
    path('login',views.login),
    path('logout',views.logout),
    path('trips/new',views.newtrip),
    path('trips/addNewTrip',views.addNewTrip),
    path('trips/delete/<int:trip_id>',views.deleteTrip),
    path('trips/<int:trip_id>',views.tripDetail),
    path('trips/edit/<int:trip_id>',views.editTrip),
    path('trips/updateTrip',views.updateTrip)


]
