from django.contrib import admin
from django.urls import path
from . import views

 


urlpatterns = [
    # 전체 편지 조회
    path('', views.LetterList.as_view()), 
    
    # receiver_pk에게 편지 작성
    # path('<int:receiver_pk>/send/', views.LetterSend.as_view()),
    
    # letter_pk 편지 디테일
    path('<int:letter_pk>/', views.LetterDetail.as_view()), 
]
