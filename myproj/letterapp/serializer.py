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