from rest_framework import serializers
from letterapp.models import letter

#모든 편지 조회
class LetterSerializer(serializers.ModelSerializer): # serializers에 있는 ModelSerializer를 상속받아 구현
    class Meta:  # Meta 클래스를 열어준다.
        model = letter
        fields = (
            'id',  
            'sendAt', 
            'sender',
            'title', 
            'content',
            'receiver',
        )

class CreateLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = letter
        fields = ['sender', 'title', 'content', 'receiver']
        
        
        
# 해당 유저 찾는 시리얼라이저 생성
        
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']  # 필요한 필드를 지정