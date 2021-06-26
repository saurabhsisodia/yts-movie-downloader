from django.urls import path
from . import views


app_name="recent_movies"

urlpatterns=[

	path('',views.index,name="index"),
]