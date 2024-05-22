from django.db import models
from django.contrib.auth.hashers import make_password

class UserModel(models.Model):
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    username = models.CharField(max_length=10, primary_key=True)
    email = models.EmailField(max_length=20)
    password = models.CharField(max_length=15)
    createdAtTime = models.TimeField(auto_now_add=True)
    createdAtDate = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.username
    
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(UserModel, self).save(*args, **kwargs)

