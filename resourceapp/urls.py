from django.urls import path
from .views import *


urlpatterns = [
    path('signup/', user_signup,),
    path('user-data/', user_signup,),
    path('login/', user_login,),
    path('available-resources/', resource_view,),
    path('get-booked-resources/', booked_resource,),
    path('book-resource/', booked_resource,),
]
