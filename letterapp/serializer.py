from rest_framework import serializers
from django.contrib.auth.models import User
from letterapp.models import letter
from datetime import datetime

#모든 편지 조회
class LetterSerializer(serializers.ModelSerializer): # serializers에 있는 ModelSerializer를 상속받아 구현
    receiver_username = serializers.CharField(source='receiver.username', read_only=True)
    sendAt = serializers.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S.%f'])
    class Meta:  # Meta 클래스를 열어준다.
        model = letter
        fields = (
            'id',  
            'sendAt', 
            'sender',
            'title', 
            'content',
            'receiver_username',
        )
        depth = 1  # User과 letter 모델의 데이터 가져옴
    
class CreateLetterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = letter
        fields = (
            'sender', 
            'title', 
            'content', 
        )

    
        
# 해당 유저 찾는 시리얼라이저 생성
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']  # 필요한 필드를 지정
        
# # 해당 유저가 오늘 받은 편지의 개수를 세주는 serializer를 만들어야 한다.