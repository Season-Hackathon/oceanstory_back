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
    path('send/<str:receiver_name>/', views.LetterSend.as_view()),
    
    # receiver_pk가 받은 모든 편지 조회
    path('list/<str:receiver_username>/',views.LetterReceiverList.as_view()),
   
    # receiver_pk가 받은 letter_pk 편지 디테일(나중에 규칙에 맞게 수정해야)
    # path('list/<str:receiver_name>/<int:letter_pk>/', views.LetterDetail.as_view()),
    path('list/<str:receiver_name>/<int:letter_pk>/', views.LetterDetail.as_view()),  
    
    
    # receiver가 오늘 받은 편지 개수 count
    path('list/count/<str:receiver_username>/', views.LetterCount.as_view())
]
