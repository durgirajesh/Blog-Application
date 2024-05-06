from django.db import models

class post_model(models.Model):
    title = models.TextField(max_length=10)
    content = models.TextField(max_length=1000)
    createdAtTime = models.TimeField(auto_now_add=True)
    createdAtDate = models.DateField(auto_now_add=True)
    updatedAtTime = models.TimeField(auto_now=True)
    updatedAtDate = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.title