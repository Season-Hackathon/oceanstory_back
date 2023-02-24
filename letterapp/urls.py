from django.contrib import admin
from django.urls import path
from . import views

 

# 앞에 letter/ 붙음 
urlpatterns = [
    # 전체 편지 조회 이건 확인용임
    path('', views.LetterList.as_view()), 
    
    # 해당 유저 찾기
    #path('users/search/<str:username>/', views.UserSearchAPIView.as_view()),
    path('search/<str:username>/', views.UserSearchAPIView.as_view()),
    
    # receiver_pk에게 편지 작성
    path('<str:receiver_name>/send/', views.LetterSend.as_view()),
    
    # receiver_pk가 받은 모든 편지 조회
    path('<str:receiver_username>/list/',views.LetterReceiverList.as_view()),
   
    # receiver_pk가 받은 letter_pk 편지 디테일
    path('<int:receiver_name>/list/<int:letter_pk>/', views.LetterDetail.as_view()), 
]
