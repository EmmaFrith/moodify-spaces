from django.db import models

class Item(models.Model):
  def __str__(self):
    return f'{self.name}'
  name = models.CharField(max_length=200)
  shop = models.CharField(max_length=200)
  image = models.CharField(max_length=400)
  owner = models.ForeignKey(
        'jwt_auth.User',
        related_name="item",
        on_delete=models.CASCADE
    )
