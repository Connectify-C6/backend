from django.urls import path
from profile_user.views import *
from report.views import *

app_name = 'report'

urlpatterns = [
    # path('all_users/', all_users, name='all_users'),
    path('report_user/<int:reported_user_id>/', report_user, name='report_user'),
    path('view_reports/', view_reports, name='view_reports'),

]