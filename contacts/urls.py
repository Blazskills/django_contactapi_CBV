from django.contrib.auth import login
from django.urls import path
from .views import ContactList,ContactDetailView 





urlpatterns = [
    path('', ContactList.as_view()),
    path('<int:id>', ContactDetailView.as_view())

]
