from django.contrib import admin
from django.urls import path, include

# from api import views
from api.views import PeopleListView, PeopleDetailView


urlpatterns = [
    # path('people-detail/', views.single_people),
    # path('people-list/', views.list_people),

    # actual views
    # path('people/<int:people_id>/', views.people_detail_view),
    # path('people/', views.people_list_view),


    path('people/', PeopleListView.as_view()),
    path('people/<int:people_id>/', PeopleDetailView.as_view()),
]
