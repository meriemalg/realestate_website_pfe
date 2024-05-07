from . import views
from django.urls import path
urlpatterns = [
    path('<int:listing_id>',views.listing,name='listing'),
    path('',views.index,name='listings') ,
  
]
