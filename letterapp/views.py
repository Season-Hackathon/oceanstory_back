from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authtoken.models import Token 
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import AccessToken

from .models import letter
from .serializer import LetterSerializer, CreateLetterSerializer
from usersapp.serializers import LoginSerializer

from rest_framework import generics
from django.contrib.auth import get_user_model
from letterapp.serializer import UserSearchSerializer
from usersapp.authenticate import SafeJWTAuthentication
from django.db.models.functions import TruncDate
from django.db.models import Count
from datetime import datetime
from django.utils.dateparse import parse_datetime

# 전체 편지 리스트 API (개발용)
class LetterList(APIView):
    authentication_classes=[SafeJWTAuthentication]
    def get(self, request):
        # letters = letter.objects.all()
        # serializer=LetterSerializer(letters, many=True)
        # return Response(serializer.data)
        letters = letter.objects.all().order_by('-sendAt')
        messages_by_date = {}
        for msg in letters:
            dt_object = parse_datetime(str(msg.sendAt))
            date_string = dt_object.date().isoformat()

            if date_string not in messages_by_date:
                messages_by_date[date_string] = []

            message_data = {
                "id": msg.id,
                "sender": msg.sender,
                "title": msg.title,
                "content": msg.content,
                "receiver_id": msg.receiver.id,
                "receiver_username": msg.receiver.username
            }

            messages_by_date[date_string].append(message_data)
        
        return Response(messages_by_date)

# receiver 편지 리스트 API
class LetterReceiverList(APIView):
    authentication_classes=[JWTAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
        
    def get(self, request, receiver_username):
        receiver  = get_object_or_404(User, username=receiver_username)
        receiver_letters=letter.objects.filter(receiver=receiver)
        # serializer=LetterSerializer(receiver_letters, many=True)
        letters = letter.objects.all().order_by('-sendAt')
        messages_by_date = {}
        for msg in letters:
            dt_object = parse_datetime(str(msg.sendAt))
            date_string = dt_object.date().isoformat()

            if date_string not in messages_by_date:
                messages_by_date[date_string] = []

            message_data = {
                "id": msg.id,
                "sender": msg.sender,
                "title": msg.title,
                "content": msg.content,
                "receiver_id": msg.receiver.id,
                "receiver_username": msg.receiver.username
            }

            messages_by_date[date_string].append(message_data)
        
        return Response(messages_by_date)
    

# 편지 개수 API
class LetterCount(APIView):
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
        
    def get(self, request, receiver_username):
        receiver  = get_object_or_404(User, username=receiver_username)
        receiver_letters=letter.objects.filter(receiver=receiver)
        letter_count = receiver_letters.count()
        return Response({'letter_count': letter_count})
        
    # def get(self, request, receiver_username):
    #     receiver = self.get_object(receiver_username)
    #     receiver_letters = letter.objects.filter(receiver=receiver)
        
    #     # annotate 메서드를 사용하여 각 날짜별로 편지 개수를 계산합니다.
    #     # TruncDate 함수를 사용하여 편지 작성 시간을 날짜로 변경하고, Count 함수를 사용하여 개수를 세어줍니다.
    #     letter_count_by_date = receiver_letters.annotate(
    #         date=TruncDate('sendAt')
    #     ).values('sendAt').annotate(
    #         count=Count('id')
    #     ).order_by('sendAt')
        
    #     # 결과를 Response 객체에 담아서 반환합니다.
    #     return Response(letter_count_by_date)
        
        
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
    # authentication_classes=[JWTAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    
    # 예외처리 해주기
    def get_object(self, letter_pk):
        try:
            return letter.objects.get(pk=letter_pk)
        except letter.DoesNotExist:
            raise Http404

    def get(self, request, letter_pk, receiver_name):  
        user = get_object_or_404(User, username=receiver_name)
        receiver=letter.objects.filter(receiver=user)
        letters=self.get_object(letter_pk)
        serializer=LetterSerializer(letters)
        return Response(serializer.data)
    

# 해당 유저를 찾는 뷰를 구현한다.
User = get_user_model()

class UserSearchAPIView(generics.RetrieveAPIView):
    serializer_class = UserSearchSerializer
    lookup_field = 'username'
    queryset = User.objects.all()