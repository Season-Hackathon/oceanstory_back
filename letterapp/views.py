from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions


from .models import letter
from .serializer import LetterSerializer, CreateLetterSerializer

from rest_framework import generics
from django.contrib.auth import get_user_model
from letterapp.serializer import UserSearchSerializer
from usersapp.authenticate import SafeJWTAuthentication

# 전체 편지 리스트 API (개발용)
class LetterList(APIView):
    authentication_classes=[SafeJWTAuthentication]
    def get(self, request):
        letters = letter.objects.all()
        serializer=LetterSerializer(letters, many=True)
        return Response(serializer.data)
        
        

# receiver 편지 리스트 API
class LetterReceiverList(APIView):
    authentication_classes=[SafeJWTAuthentication]
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
        
    def get(self, request, receiver_username):
        username = get_object_or_404(User, username=receiver_username)
        receiver_letters=letter.objects.filter(receiver=username)
        serializer=LetterSerializer(receiver_letters, many=True)
        return Response(serializer.data)
    
    
        
# 편지 작성 API    
class LetterSend(APIView):
    def post(self, request, receiver_name):
        user = get_object_or_404(User, username=receiver_name)
        serializer=CreateLetterSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save(receiver=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
# 편지 하나씩 볼 수 있음(Token 처리하면 편할듯)    
class LetterDetail(APIView):
    authentication_classes=[SafeJWTAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    # 예외처리 해주기
    def get_letter(self, letter_pk):
        try:
            return letter.objects.get(pk=letter_pk)
        except letter.DoesNotExist:
            raise Http404
        
    def get(self, request, letter_pk, receiver_name):
        receiver_pk=letter.objects.filter(receiver=receiver_name)
        Letters=self.get_letter(letter_pk)
        serializer=LetterSerializer(Letters)
        return Response(serializer.data)
        
    

# 해당 유저를 찾는 뷰를 구현한다.
User = get_user_model()

class UserSearchAPIView(generics.RetrieveAPIView):
    serializer_class = UserSearchSerializer
    lookup_field = 'username'
    queryset = User.objects.all()