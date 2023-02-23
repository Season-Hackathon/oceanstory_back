from django.shortcuts import render
from django.contrib.auth.models import User    # 이걸 그냥 가져다 쓴다.(민우)
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import letter
from .serializer import LetterSerializer, CreateLetterSerializer



class LetterList(APIView):
    def get(self, request):
        letters = letter.objects.all()
        serializer=LetterSerializer(letters, many=True)
        return Response(serializer.data)
        
    # for letter in letters:
        # 여기에 디데이.. 편지 공개 날짜 설정

# 편지 쓰기 API는 다시 해봐야할듯. admin으로 일단 해봄
# class LetterSend(APIView):


# 편지 하나씩 볼 수 있음(pk 값으로)
class LetterDetail(APIView):
    # 예외처리 해주기
    def get_letter(self, letter_pk):
        try:
            return letter.objects.get(pk=letter_pk)
        except letter.DoesNotExist:
            raise Http404
        
    def get(self, request, letter_pk):
        letter=self.get_letter(letter_pk)
        serializer=LetterSerializer(letter)
        return Response(serializer.data)
    
    
    
# 해당 유저를 찾는 뷰를 구현한다.
from rest_framework import generics
from django.contrib.auth import get_user_model
from letterapp.serializer import UserSearchSerializer

User = get_user_model()

class UserSearchAPIView(generics.RetrieveAPIView):
    serializer_class = UserSearchSerializer
    lookup_field = 'username'
    queryset = User.objects.all()