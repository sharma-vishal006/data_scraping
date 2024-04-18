from django.urls import path
from .views import ExtractImageFromDoc,Msgtoword

urlpatterns = [
    path('img/', ExtractImageFromDoc.as_view(), name='extract-img-from-doc'),
    path('msgtoword/',Msgtoword.as_view(),name='word'),
    
    
]
