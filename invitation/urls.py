from django.urls import path
from invitation.views import *

app_name = 'invitation'

urlpatterns = [
    path('', index, name='index'),
    ]