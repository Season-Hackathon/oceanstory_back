from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
# import datetime
from django.utils import timezone

# Create your models here.
class letter(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='letter_id')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    
    sender = models.CharField(verbose_name='보내는 사람', max_length=10)    # 작성자
    title = models.CharField(verbose_name='편지 제목', max_length=50) # 제목/길이제한o
    content = models.TextField(verbose_name='편지 내용')    # 본문/길이제한x
    
    # 한국 시간 구하기
    sendAt = models.DateTimeField(default=timezone.now) 
    
    # 편지 확인 여부
    isOpened = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'letter'
        
    def __str__(self):
        return self.title   # 데이터를 불러올때
    
    